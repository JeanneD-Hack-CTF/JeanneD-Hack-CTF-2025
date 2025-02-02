#ifndef STRING__H

typedef struct String String;

String *new_string(const char *str);
String *new_string_from(char *str, size_t size);
uint64_t hash_string(String *s);
void serialize_string(String *s, FILE *fp);
String *deserialize_string(FILE *fp);
size_t string_get_size(String *s);
const char *string_get_str(String *s);
void free_string(String **s);

#endif // !STRING__H
