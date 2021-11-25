/**
 * @author Srijan Mukherjee
 * 
 * Problem Statement: Program to copy an array to another array
 */

#include <stdio.h>

int main()
{
    int n; // size of array

    printf("size of array: ");
    scanf("%d", &n);

    if (n <= 0) {
        printf("ERROR: number of elements must be positive");
        return 0;
    }

    int arr[n];
    int copy[n];

    // input array
    printf("Enter %d array entries\n", n);
    for (int i = 0; i < n; i++) {
        printf("arr[%d]: ", i);
        scanf("%d", &arr[i]);
    }

    printf("[INFO] copying the array\n");

    for (int i = 0; i < n; i++) {
        copy[i] = arr[i];
    }

    printf("Copied array: { ");

    for (int i = 0; i < n; i++) {
        if (i > 0) printf(", ");
        printf("%d", copy[i]);
    }

    printf(" }\n");

    return 0;
}
