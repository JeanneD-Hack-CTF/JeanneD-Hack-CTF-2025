#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/mman.h>
#include <sys/ptrace.h>

#include "embedded.h"

#define ERROR       -42
#define SUCCESS       0
 
extern unsigned char program[];
extern unsigned int program_len; 

int check_password(int argc, char *argv[], char *envp[]) {
    int res = ERROR;
    int pid = fork();
    if (pid == -1) {
        res = ERROR;
    }    
    else if (pid == 0) {
        // Child
        int trace = ptrace(PTRACE_TRACEME,0,0);
        if (trace == 0) {
            // No debbuger, create an anonymous file in memory
            int elf = memfd_create("", 0);
            if (elf > 0) {
                // Write the program to it
                write(elf, program, program_len); 
                // Exec child
                fexecve(elf, argv, envp); 
            }
            res = SUCCESS;
        } else {
            res = ERROR;
        } 
    } else {
        // Parent
        wait(NULL);
        res = SUCCESS;
    }
    return res;
}

int main(int argc, char *argv[], char *envp[]) {
    if (argc != 2) {
        printf("Usage: %s <password>\n", argv[0]);
        return ERROR;
    }
    if (check_password(argc, argv, envp) != SUCCESS) {
        printf("Wrong password\n");
        return ERROR;
    }
    return SUCCESS;
}
