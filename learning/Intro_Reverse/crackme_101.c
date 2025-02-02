#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Password is IN7ro_au_Rev3rSe
int check_password(const char *password) {
  if (strlen(password) != 16) {
    return EXIT_FAILURE;
  }
  if (password[0] == 'I' && password[1] == 'N') {
    if (password[2] == '7' && password[3] == 'r') {
      if (password[4] == 'o' && password[5] == '_') {
        if (strncmp("au_Rev3rSe", password+6, 11) == 0) {
          return EXIT_SUCCESS;
        } 
      }
    }
  }
  return EXIT_FAILURE;
}

int main(int argc, const char *argv[]) {
  if (argc != 2) {
    fprintf(stderr, "Usage: %s <password>\n", argv[0]);
    return EXIT_SUCCESS;
  }
  
  if (check_password(argv[1]) != EXIT_SUCCESS) {
    fprintf(stderr, "Wrong password!\n");
  } else {
    fprintf(stderr, "Congratulations! You can validate with:\n");
    fprintf(stderr, "JDHACK{%s}\n", argv[1]);
  }
  return EXIT_SUCCESS;
}
