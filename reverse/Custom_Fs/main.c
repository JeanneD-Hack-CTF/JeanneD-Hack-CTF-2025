#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <stdbool.h>

#include "custom_fs.h"

bool is_directory(const char *dname) {
	struct stat st;
  if (lstat(dname, &st) == -1) {
    return false;
  }
  return S_ISDIR(st.st_mode);
}

bool is_file(const char *file) {
  return access(file, F_OK) == 0;
}

int main(int argc, const char *argv[]) {
  if (argc != 4) {
    fprintf(stderr, "Usage: %s CMD\n", argv[0]);
    fprintf(stderr, "Available commandes:\n");
    fprintf(stderr, "  pack <directory> <file>\n");
    fprintf(stderr, "  unpack <file> <directory>\n");
    return EXIT_SUCCESS;
  }

  if (strncmp("pack", argv[1], 5) == 0) {
    // Unsure argument is a directory
    if (!is_directory(argv[2])) {
      fprintf(stderr, "Error: '%s' is not a valid directory\n", argv[2]);
      return EXIT_FAILURE;
    }

    CustomFs *fs = new_filesystem(argv[2]);
    if (fs != NULL) {  
      if (pack_filesystem(fs, argv[2]) != EXIT_SUCCESS || serialize_filesystem(fs, argv[3]) != EXIT_SUCCESS) {
        fprintf(stderr, "Fail to save filesystem to '%s'\n", argv[3]);
      }
      free_filesystem(&fs);
    }

  } else if (strncmp("unpack", argv[1], 7) == 0) {
#ifdef DEBUG
    if (!is_file(argv[2])) {
      fprintf(stderr, "Error: '%s' does not exists\n", argv[2]);
      return EXIT_FAILURE;
    }

    CustomFs *fs = deserialize_filesystem(argv[2]);
    if (fs != NULL) {
      if (unpack_filesystem(fs, argv[3]) != EXIT_SUCCESS) {
        fprintf(stderr, "Fail to unpack '%s' to '%s'\n", argv[2], argv[3]);
      }
      free_filesystem(&fs);
    } else {
      fprintf(stderr, "Fail to load filesystem '%s'\n", argv[2]);
    }
#else 
    fprintf(stderr, "Error: Not implemented\n");
    return EXIT_FAILURE;
#endif 

  } else {
    fprintf(stderr, "Error: Unknown command '%s'\n", argv[1]);
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
