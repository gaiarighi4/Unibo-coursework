#include <iostream>
using namespace std;

int dup(int A[], int n, int j, int l){
    if(j >= l){
        return 0;
    }else if(A[j] == n){
        return 1 + dup(A, n, j+1, l);
    }else{
        return dup(A, n, j+1, l);
    }
}

bool tre_copie(int A[], int j, int l){
    if(j >= l){
        return false;
    }else if(dup(A, A[j], 0, l) >= 3){
        return true;
    }else{
        return tre_copie(A, j+1, l);
    }
}


struct Lista_di_interi{
    int val;
    Lista_di_interi *next;
};
typedef Lista_di_interi * lista;

lista concatena_it(lista L1, lista L2){
    if(L1 == NULL){
        return L2;
    }
    if(L2 == NULL){
        return L1;
    }
    lista tmp = L1;
    while(tmp->next != NULL){
        tmp = tmp->next;
    }
    tmp->next = L2;
    return L1;
}

lista concatena_ric(lista L1, lista L2){
    if(L1 == NULL){
        return L2;
    }
    if(L2 == NULL){
        return L1;
    }
    if(L1->next == NULL){
        L1->next = L2;
        return L1;
    }
    L1->next = concatena_ric(L1->next, L2);
    return L1;
}


//L'esercizio 3 è impossibile da fare