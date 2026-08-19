#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    printf("Phishing URL Scanner - Process Manager\n");

    pid_t pid = fork();

    if (pid < 0)
    {
        printf("Process creation failed.\n");
        return 1;
    }
    else if (pid == 0)
    {
        // Child process
        printf("Child process: Scanning URL...\n");

        // Later, the phishing URL scanning code will go here.

        printf("Child process: Scan completed.\n");
        exit(0);
    }
    else
    {
        // Parent process
        printf("Parent process: Waiting for scanner...\n");

        wait(NULL);

        printf("Parent process: Scanner finished.\n");
    }

    return 0;
}
