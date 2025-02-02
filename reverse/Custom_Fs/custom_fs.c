#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <inttypes.h>
#include <time.h> 
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <dirent.h>

#include "string.h"
#include "hashtree.h"
#include "custom_fs.h"

#define EXIT_SUCCESS          0
#define EXIT_ERROR           -1

#define FS_VERSION       0x1337
#define CUSTOM_FS_NAME       32

#define MIN(x, y)       ((x) < (y) ? (x) : (y))

struct CustomFs {
  uint16_t  version;
  uint8_t   name[CUSTOM_FS_NAME];
  HashTree *entries;
  HashTree *chunks;
};

CustomFs *new_filesystem(const char *name) {
  CustomFs *fs = malloc(sizeof(*fs));
  if (fs != NULL) {
    fs->version = FS_VERSION;
    memcpy(fs->name, name, MIN(strlen(name), CUSTOM_FS_NAME));
    fs->entries = new_hashtree();
    fs->chunks = new_hashtree();
    if (fs->chunks == NULL || fs->entries == NULL) {
      if (fs->chunks != NULL) {
        free_hashtree(&fs->chunks);
      }
      if (fs->entries != NULL) {
        free_hashtree(&fs->entries);
      }
      fs = NULL;
    }
  }
  return fs;
}

void free_filesystem(CustomFs **fs) {
  if (fs != NULL && *fs != NULL) {
    free_hashtree(&(*fs)->chunks);
    free_hashtree(&(*fs)->entries);
    free(*fs);
    *fs = NULL;
  }
}

int add_normal_file_to_filesystem(CustomFs *fs, const char *filename, size_t size) {
  char buffer[FILENAME_MAX + 4] = "FILE";
  memcpy(buffer+4, filename, MIN(strlen(filename), FILENAME_MAX));

  // Create an entry for the filename
  String *entry = new_string(buffer);
  if (entry == NULL) {
    return EXIT_ERROR;
  }

  // Read file content 
  void *tmp_buffer = malloc(size + 1);
  if (tmp_buffer == NULL) {
    free_string(&entry);
    return EXIT_ERROR;
  }

  // Open file
  FILE *fp = fopen(filename, "r");
  if (fp == NULL) {
    free_string(&entry);
    free(tmp_buffer);
    return EXIT_ERROR;
  }

  // Read file content 
  if (fread(tmp_buffer, size, 1, fp) != 1) {
    free_string(&entry);
    free(tmp_buffer);
    fclose(fp);
    return EXIT_ERROR;
  } 

  // Close file handle 
  fclose(fp);
  String *chunk = new_string_from(tmp_buffer, size);
  if (chunk == NULL) {
    free_string(&entry);
    free(tmp_buffer);
    return EXIT_ERROR;
  }

  // Compute key for both node
  uint64_t key = hash_string(entry);
  TreeNode *entry_node = new_node(key, entry);
  if (entry_node == NULL) {
    free_string(&entry);
    free_string(&chunk);
    return EXIT_ERROR;
  }

  TreeNode *chunk_node = new_node(key, chunk);
  if (chunk_node == NULL) {
    free_node(&entry_node);
    free_string(&entry);
    free_string(&chunk);
    return EXIT_ERROR;
  }

  // Insert nodes
  insert_hashtree(fs->entries, entry_node);
  insert_hashtree(fs->chunks, chunk_node);
  return EXIT_SUCCESS;
}

int add_directory_to_filesystem(CustomFs *fs, const char *directory) {
  char buffer[FILENAME_MAX + 4] = "DIR ";
  memcpy(buffer+4, directory, MIN(strlen(directory), FILENAME_MAX));

  // Create an entry for the filename
  String *entry = new_string(buffer);
  if (entry == NULL) {
    return EXIT_ERROR;
  }

  // Compute key for node
  uint64_t key = hash_string(entry);
  TreeNode *entry_node = new_node(key, entry);
  if (entry_node == NULL) {
    free_string(&entry);
    return EXIT_ERROR;
  }
  
  insert_hashtree(fs->entries, entry_node);
  return EXIT_SUCCESS;
}

int add_link_to_filesystem(CustomFs *fs, const char *from, const char *to) {
  char buffer[FILENAME_MAX * 2 + 5] = "LINK";
  size_t from_size = MIN(strlen(from), FILENAME_MAX);
  memcpy(buffer+4, from, from_size);
  buffer[4+from_size] = '#'; // Marker 
  memcpy(buffer+4+from_size+1, to, MIN(strlen(to), FILENAME_MAX));

  // Create an entry for the filename
  String *entry = new_string(buffer);
  if (entry == NULL) {
    return EXIT_ERROR;
  }
    
  // Compute key for node
  uint64_t key = hash_string(entry);
  TreeNode *entry_node = new_node(key, entry);
  if (entry_node == NULL) {
    free_string(&entry);
    return EXIT_ERROR;
  }

  insert_hashtree(fs->entries, entry_node);
  return EXIT_SUCCESS;
}

int add_to_filesystem(CustomFs *fs, const char *filename) {
  char buffer[FILENAME_MAX];
  struct stat st;
  if (lstat(filename, &st) != 0) {
    // Fail to stat file, exit
    return EXIT_ERROR;
  }

  if (S_ISLNK(st.st_mode)) {
    ssize_t link_size = readlink(filename, buffer, sizeof(buffer));
    if (link_size < 0) {
      return EXIT_ERROR;
    }
    buffer[link_size] = 0;
    return add_link_to_filesystem(fs, filename, buffer);
  } else if (S_ISDIR(st.st_mode)) {
    return add_directory_to_filesystem(fs, filename);
  } else {
    return add_normal_file_to_filesystem(fs, filename, st.st_size);
  }
  return EXIT_SUCCESS;
}

// Helper function that recursively call the callback on each file of the given directory
int __walk_recur(const char *dname, void (*func)(void *, char *), void *ctx) {
	struct dirent *dent;
	struct stat st;
	DIR *dir;
	char fn[FILENAME_MAX];

  // Check for file length
	int len = strlen(dname);
	if (len >= FILENAME_MAX - 1) {
		return EXIT_ERROR;
  }

	strcpy(fn, dname);
	fn[len++] = '/';

	if (!(dir = opendir(dname))) {
		fprintf(stderr, "can't open %s\n", dname);
		return EXIT_ERROR;
	}

	while ((dent = readdir(dir))) {
		if (dent->d_name[0] == '.')
			continue;
		if (!strcmp(dent->d_name, ".") || !strcmp(dent->d_name, ".."))
			continue;

		strncpy(fn + len, dent->d_name, FILENAME_MAX - len);
		if (lstat(fn, &st) == -1) {
		  fprintf(stderr, "can't stat %s\n", fn);
			continue;
		}

		// Will be false for symlinked dirs
		if (S_ISDIR(st.st_mode)) {
      // Abort on error
			if (__walk_recur(fn, func, ctx) != EXIT_SUCCESS) {
        return EXIT_ERROR;
      }
		}      
    // Call user callback
    func(ctx, fn);
	}

	if (dir) { 
    closedir(dir);
  }
	return EXIT_SUCCESS;
}

int pack_filesystem(CustomFs *fs, const char *directory) {
  int result = EXIT_ERROR;
  if (fs != NULL && directory != NULL) {
    result = __walk_recur(directory, (void (*)(void *, char *))add_to_filesystem, fs);
  }
  return result;
}

int serialize_filesystem(CustomFs *fs, const char *file) {
  FILE *fp = fopen(file, "w");
  if (fp == NULL) {
    return EXIT_ERROR;
  }
 
  fwrite(&(fs->version), sizeof(fs->version), 1, fp);
  fwrite(fs->name, CUSTOM_FS_NAME, 1, fp);
  serialize_hashtree(fs->entries, (void (*)(void *, FILE *))serialize_string, fp);
  serialize_hashtree(fs->chunks, (void (*)(void *, FILE *))serialize_string, fp);
  fclose(fp);
  return EXIT_SUCCESS;
}

#ifdef DEBUG 


static void _mkdir(const char *dir) {
  char tmp[FILENAME_MAX];
  char *p = NULL;
  size_t len;

  snprintf(tmp, sizeof(tmp), "%s", dir);
  len = strlen(tmp);
  if (tmp[len - 1] == '/') {
    tmp[len - 1] = 0;
  }
  for (p = tmp + 1; *p; p++) {
    if (*p == '/') {
      *p = 0;
      mkdir(tmp, S_IRWXU);
      *p = '/';
    }
  }
  mkdir(tmp, S_IRWXU);
}

void create_directories(TreeNode *node, void *unused) {
  String *s = get_node_value(node);
  const char *filename = string_get_str(s);
  if (filename != NULL && strncmp(filename, "DIR", 3) == 0) {
    // Recursively create directory
    _mkdir(filename+4);
  }
}

void create_files(TreeNode *node, void *ctx) {
  CustomFs *fs = (CustomFs *)ctx;
  String *s = get_node_value(node);
  const char *filename = string_get_str(s);
  if (filename != NULL && strncmp(filename, "FILE", 4) == 0) {
    // Search for chunk corresponding to entry
    TreeNode *chunk_node = find_hashtree(fs->chunks, get_node_key(node));
    if (chunk_node == NULL) {
      fprintf(stderr, "Error: Fail to find chunk associated with '%s'\n", filename+4);
    } else {
      // Create file 
      String *chunk = get_node_value(chunk_node);
      FILE *fp = fopen(filename+4, "w");
      if (fp != NULL) {
        fwrite(string_get_str(chunk), string_get_size(chunk), 1, fp);
        fclose(fp);
      }
    }
  }
}

void create_links(TreeNode *node, void *unused) {
  String *s = get_node_value(node);
  const char *filename = string_get_str(s);
  if (filename != NULL && strncmp(filename, "LINK", 4) == 0) {
    // Create symlink
    char *from = strstr(filename+4, "#"); 
    if (from != NULL) {
      *from = 0; 
      symlink(from+1, filename+4);
      *from = '#';
    }
  }
}

int unpack_filesystem(CustomFs *fs, const char *directory) {
  int result = EXIT_ERROR;
  if (fs != NULL && directory != NULL) {
    dfs_hashtree(fs->entries, create_directories, NULL);
    dfs_hashtree(fs->entries, create_files, fs);
    dfs_hashtree(fs->entries, create_links, NULL);
    result = EXIT_SUCCESS;
  }
  return result;
}

CustomFs *deserialize_filesystem(const char *file) {
  FILE *fp = fopen(file, "r");
  if (fp == NULL) {
    return NULL;
  }
 
  CustomFs *fs = malloc(sizeof(*fs));
  if (fs != NULL) {
    if (fread(&(fs->version), sizeof(fs->version), 1, fp) != 1 || fread(fs->name, CUSTOM_FS_NAME, 1, fp) != 1) {
      free(fs);
      fs = NULL;
    } else {
      fs->entries = deserialize_hashtree((void *(*)(FILE *))deserialize_string, fp);
      fs->chunks = deserialize_hashtree((void *(*)(FILE *))deserialize_string, fp);
    }
  }
  fclose(fp);
  return fs;
}

#endif 
