#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#include "string.h"

struct String {
  size_t size;  // Size of the string 
  char  *str;   // The read string buffer
};

String *new_string(const char *str) {
  String *s = malloc(sizeof(*s));
  if (s != NULL) {
    s->size = strlen(str);
    s->str = malloc(s->size + 1);
    if (s->str == NULL) {
      free(s);
      s = NULL;
    } else {
      memcpy(s->str, str, s->size);
      s->str[s->size] = 0;
    }
  }
  return s;
}

String *new_string_from(char *str, size_t size) {
  String *s = malloc(sizeof(*s));
  if (s != NULL) {
    s->size = size;
    s->str = str;
  }
  return s;
}

#define FNV_OFFSET 14695981039346656037UL
#define FNV_PRIME 1099511628211UL

// Return 64-bit FNV-1a hash for key (NUL-terminated). See description:
// https://en.wikipedia.org/wiki/Fowler–Noll–Vo_hash_function
uint64_t hash_string(String *s) {
    uint64_t hash = FNV_OFFSET;
    for (size_t i = 0; i < s->size; ++i) {
        hash ^= (uint64_t)(unsigned char)(s->str[i]);
        hash *= FNV_PRIME;
    }
    return hash;
}

const char *string_get_str(String *s) {
  // Getter for inner wrapped string
  return s == NULL ? NULL : s->str;
}

size_t string_get_size(String *s) {
  return s == NULL ? 0 : s->size;
}

void serialize_string(String *s, FILE *fp) {
  if (s != NULL && fp != NULL) {
    fwrite(&(s->size), sizeof(s->size), 1, fp);
    fwrite(s->str, s->size, 1, fp);
  }
}

String *deserialize_string(FILE *fp) {
  String *s = NULL;
  if (fp != NULL) {
    s = malloc(sizeof(*s));
    if (s != NULL) {
      fread(&(s->size), sizeof(s->size), 1, fp);
      s->str = malloc(s->size + 1);
      if (s->str == NULL) {
        free(s);
        s = NULL;
      } else {
        fread(s->str, s->size, 1, fp);
        s->str[s->size] = 0;
      }
    }
  }
  return s;
}

void free_string(String **s) {
  if (s != NULL && *s != NULL) {
    free(*s);
    *s = NULL;
  }
}
