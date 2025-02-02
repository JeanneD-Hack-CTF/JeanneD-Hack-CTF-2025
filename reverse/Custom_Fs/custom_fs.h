#ifndef CUSTOM_FS__H

typedef struct CustomFs CustomFs;

CustomFs *new_filesystem(const char *name);
int add_to_filesystem(CustomFs *fs, const char *filename);

int pack_filesystem(CustomFs *fs, const char *directory); 
int serialize_filesystem(CustomFs *fs, const char *file);

#ifdef DEBUG 
int unpack_filesystem(CustomFs *fs, const char *directory);
CustomFs *deserialize_filesystem(const char *file);
#endif 

void free_filesystem(CustomFs **fs);

#endif // !CUSTOM_FS__H
