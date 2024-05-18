#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Reserve 5 byte of buffer plus the terminating NULL.
    // should allocate 8 bytes = 2 double words,
    char buffer[5]; // no more than 8 characters input
    if (argc < 2)
    {
        printf("strcpy() NOT executed.\n");
        printf("Syntax: %s <characters>\n", argv[0]);
        exit(0);
    }
    
    strcpy(buffer, argv[1]); // copy the user input to buffer;
                             // without checking any size
                             // if you want to try strcpy() safely...
                             
    printf("buffer content= %s\n", buffer);
    
    // you may want to try strcat()...
    
}