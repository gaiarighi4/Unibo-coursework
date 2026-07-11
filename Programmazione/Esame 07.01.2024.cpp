#include <iostream>
using namespace std;

void scambia(int A[], int j, int l){
    if(j >= l){
        return;
    }else if(A[j] % 2 != 0){
        scambia(A, j+1, l);
    }else if(A[l] % 2 == 0){
        scambia(A, j, l-1);
    }else{
        int tmp = A[j];
        A[j] = A[l];
        A[l] = tmp;

        scambia(A, j+1, l-1);
    }
}

void dispari_prima_di_pari(int A[], int l){
    scambia(A, 0, l-1);
}



//ITERATIVA
bool no_pari_dup(int A[], int l){
    for(int i=0; i<l; i++){
        if(A[i] % 2 == 0){
            for(int j=i+1; j<l; j++){
                if(A[j] == A[i]){
                    return false;
                }
            }
        }
    }
    return true;
}


//RICORSIVA
int dup(int A[], int n, int j, int l){
    if(j >= l){
        return 0;
    }else if(A[j] == n){
        return 1 + dup(A, n, j+1, l);
    }else{
        return dup(A, n, j+1, l);
    }
}
bool no_pari_dup(int A[], int length){
    for(int i=0; i<length; i++){
        if(A[i]%2 == 0){
            int ndup = dup(A, A[i], 0, length-1);
            if(ndup > 1){
                return false;
            }
        }
    }
    return true;
}
