#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ERROR       -42
#define SUCCESS       0
 
int check_password(char *pwd) {
    const char *ref = "y0u_r34ch_7h3_l457_l3v3l!"; 
    if (strncmp(pwd, ref, strlen(ref)) == 0) {
        printf("\nCongratulations, you can validate with:\n");
        printf("JDHACK{%s}\n", ref);
        return SUCCESS;
    }
    return ERROR;
}

// Password: y0u_r34ch_7h3_l457_l3v3l!
int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <password>\n", argv[0]);
        return ERROR;
    }
    if (check_password(argv[1]) != SUCCESS) {
        printf("\nWrong password\n");
        return ERROR;
    }
    return SUCCESS;
}
