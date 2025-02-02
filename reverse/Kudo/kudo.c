#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>
#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>

#define EXIT_SUCCESS      0
#define EXIT_ERROR       -1
#define BUFFER_SIZE    1024

#define KEY_LENGTH       32
#define IV_LENGTH        16

#define SHADOW_FILE     "./shadow"

#define MIN(x, y)       ((x) < (y) ? (x) : (y))

void handleErrors(void) {
    ERR_print_errors_fp(stderr);
    abort();
}

int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
            unsigned char *iv, unsigned char *ciphertext) {
    EVP_CIPHER_CTX *ctx;

    int len;

    int ciphertext_len;

    /* Create and initialise the context */
    if(!(ctx = EVP_CIPHER_CTX_new()))
        handleErrors();

    /*
     * Initialise the encryption operation. IMPORTANT - ensure you use a key
     * and IV size appropriate for your cipher
     * In this example we are using 256 bit AES (i.e. a 256 bit key). The
     * IV size for *most* modes is the same as the block size. For AES this
     * is 128 bits
     */
    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv))
        handleErrors();

    /*
     * Provide the message to be encrypted, and obtain the encrypted output.
     * EVP_EncryptUpdate can be called multiple times if necessary
     */
    if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len))
        handleErrors();

    ciphertext_len = len;

    /*
     * Finalise the encryption. Further ciphertext bytes may be written at
     * this stage.
     */
    if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len))
        handleErrors();

    ciphertext_len += len;

    /* Clean up */
    EVP_CIPHER_CTX_free(ctx);

    return ciphertext_len;
}

void hexencode(char *str, size_t len, char *result, size_t size) {
  // Check if the result array is large enough
  if ((len * 2) > size - 1) {
    return;
  }
    
  // Iterate over the string
  for (size_t i = 0; i < len; i++) {
    char hex[128];
    // Convert character to hexadecimal
    sprintf(hex, "%02x", str[i]);
    memcpy(result + i*2, hex, 2);
  }
}

char *base64_encode(const char *message, size_t size) {
    int encodedSize = 4 * ceil((double)size / 3);
    char *buffer = malloc(encodedSize + 1);
    
    if (buffer == NULL) {
      return NULL;
    }

    BIO *bio, *b64;
    FILE *stream;

    stream = fmemopen(buffer, encodedSize + 1, "w");

    b64 = BIO_new(BIO_f_base64());
    bio = BIO_new_fp(stream, BIO_NOCLOSE);
    bio = BIO_push(b64, bio);

    // Ignore newlines - write everything in one line
    BIO_set_flags(bio, BIO_FLAGS_BASE64_NO_NL); 

    BIO_write(bio, message, size);
    BIO_flush(bio);

    BIO_free_all(bio);
    fclose(stream);

    return buffer; 
}

int compare_password(char *username, char *password, char *hashed) {
  char buffer[BUFFER_SIZE];
  char encrypted[BUFFER_SIZE];
  char username_buffer[BUFFER_SIZE*2];
  char iv[IV_LENGTH] = "58ee6d5465a345d1";
  size_t len = strlen(password);

  // Step 1: Swap some of the character
  for (size_t i = 0; i < len; ++i) {
    if (password[i] == '_') {
      password[i] = '/';
    } else if (password[i] == '/') {
      password[i] = '_'; 
    } else if (password[i] == '+') {
      password[i] = '-';
    } else if (password[i] == '-') {
      password[i] = '+';
    } else if (password[i] == '!') {
      password[i] = '?';
    } else if (password[i] == '?') {
      password[i] = '!';
    } else if (password[i] == '#') {
      password[i] = '@';
    } else if (password[i] == '@') {
      password[i] = '#';
    }
  }

  // Step 2: Crapto xor
  for (size_t i = len; i > 0; --i) {
    password[i] = password[i] ^ i; 
  }
  
  // Step 3: Encode as hex 
  hexencode(password, len, buffer, BUFFER_SIZE); 
  len *= 2;

  // Step 4: Encrypt password using username

  // Expand username if not long enough 
  for (size_t i = 0; i < KEY_LENGTH; i++) {
    username_buffer[i] = username[i % strlen(username)];
  }

  int encrypted_len = encrypt(buffer, len, username_buffer, iv, encrypted);

  // Step 5: Encode result as base64 (to be able to put it in the file)
  char *out = base64_encode(encrypted, encrypted_len);
  if (out != NULL) {
    fprintf(stderr, "DEBUG: %s\n", out);
    int compare = memcmp(out, hashed, 24);
    free(out);
    return compare == 0 ? EXIT_SUCCESS : EXIT_ERROR;
  }
  return EXIT_ERROR;
}

int login(char *username, char *password) {
  int auth_result = EXIT_ERROR;
  char buffer[BUFFER_SIZE];
  // Backup password because it will be modified by compare_password
  char password_buffer[BUFFER_SIZE];
  memcpy(password_buffer, password, strlen(password));

  // Open file 
  FILE *fp = fopen(SHADOW_FILE, "r");
  if (fp == NULL) {
    printf("ERROR: could not open %s\n", SHADOW_FILE);
    return EXIT_ERROR;
  }
  // Read line by line
  while (fgets(buffer, sizeof(buffer), fp)) {
    size_t idx = strcspn(buffer, ":");
    if (strncmp(username, buffer, idx) == 0) {
      auth_result = compare_password(username, password_buffer, buffer+idx+1+4); 
      break;
    }
  }

  // Close file handle
  fclose(fp);

  return auth_result;
}

int main(void) {
  printf(
   "                                        \n"
   " __    __                 __            \n" 
   " |  \\  /  \\               |  \\          \n"
   " | $$ /  $$__    __   ____| $$  ______  \n"
   " | $$/  $$|  \\  |  \\ /      $$ /      \\ \n"
   " | $$  $$ | $$  | $$|  $$$$$$$|  $$$$$$\\\n"
   " | $$$$$\\ | $$  | $$| $$  | $$| $$  | $$\n"
   " | $$ \\$$\\| $$__/ $$| $$__| $$| $$__/ $$\n"
   " | $$  \\$$\\\\$$    $$ \\$$    $$ \\$$    $$\n"
   "  \\$$   \\$$ \\$$$$$$   \\$$$$$$$  \\$$$$$$  \n\n"
   "    Strong login prompt (better than sudo)    \n\n"
  );

  char username[BUFFER_SIZE];
  char password[BUFFER_SIZE];

  // Prompting for username
  printf("Enter your username: ");
  fgets(username, sizeof(username), stdin);

  // Removing trailing newline character added by fgets
  username[strcspn(username, "\n")] = '\0';

  // Prompting for password
  printf("Enter your password: ");
  fgets(password, sizeof(password), stdin);

  // Removing trailing newline character added by fgets
  password[strcspn(password, "\n")] = '\0';
  
  if (login(username, password) == EXIT_SUCCESS) {
    printf("Welcome back %s!\n", username);
    printf("Here is your flag: JDHACK{%s}\n", password);
  } else {
    printf("Authentification failure\n");
  }


  return EXIT_SUCCESS;
}
