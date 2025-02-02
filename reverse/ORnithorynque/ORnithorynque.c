#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void flagxor(void);

int main(void) {
    printf("See you at this location : ");
    flagxor();
    return 0;
}

void flagxor(void) {
    int FLAG[] = {
        0x4B, 0x45, 0x49, 0x42, 0x44, 0x4C, 0x7C, 0x55, 
        0x70, 0x4C, 0x5A, 0x70, 0x60, 0x54, 0x69, 0x4A, 0x43, 
        0x76, 0x5A, 0x62, 0x7E, 0x52, 0x52, 0x52, 0x52, 0x52, 0x52, 0x52, 0x52, 
        0x52, 0x52, 0x52, 0x52, 0x52, 0x52, 0x52, 0x52  
    };
    int size = sizeof(FLAG) / sizeof(int);
    for(int i = 0; i < size; ++i) {
        FLAG[i] -= 0x01;
    }
    size = 21;
    char flag[50];
    int cpt = 0;
    for(int i = 0; i < size; ++i) {
        flag[cpt] = (char)(FLAG[i] ^ 0x03); 
        ++cpt;
    }
    for(int i = 0; i < size; ++i) {
        flag[i] = (char)(flag[i] ^ 0x06);
    }
    flag[size] = '\0';
    printf("%s\n", flag);
}
