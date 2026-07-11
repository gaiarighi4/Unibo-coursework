#include <iostream>
using namespace std;

#define N 100
#define MAX_SIZE 1000

bool bilanciata(char str[]){
    char stack[MAX_SIZE];  // Array che simula lo stack
    int top = -1;  // Indice per la cima dello stack

    for(int i = 0; str[i] != '\0'; i++){
        char c = str[i];

        // Se è una parentesi aperta, aggiungila allo stack
        if(c == '(' || c == '[' || c == '{'){
            if(top < MAX_SIZE){  // Verifica se lo stack non è pieno
                stack[++top] = c;
            }
        }
            // Se è una parentesi chiusa
        else if(c == ')' || c == ']' || c == '}'){
            // Se lo stack è vuoto o la parentesi non corrisponde, non è bilanciato
            if(top == -1){
                return false;
            }
            char apertura = stack[top--];  // Rimuove la parentesi in cima allo stack

            // Controlla se la parentesi chiusa corrisponde alla parentesi aperta
            if ((c == ')' && apertura != '(') ||
                (c == ']' && apertura != '[') ||
                (c == '}' && apertura != '{')) {
                return false;
            }
        }
    }
    // Alla fine, lo stack deve essere vuoto per essere bilanciato
    return top == -1;
}


struct Istruzione{
    char descrizione[N];
    bool pezzi[50];
    Istruzione* next;
};
typedef Istruzione * lista;

lista remove_istruzioni(lista L, char d[]){
    lista curr = L;
    lista prec = NULL;

    while(curr != NULL){
        if(strcmp(curr->descrizione, d) == 0){
            if(prec == NULL){
                L = L->next;
                delete curr;
                curr = L;
            }else{
                prec->next = curr->next;
                delete curr;
                curr = prec->next;
            }
        }else{
            prec = curr;
            curr = curr->next;
        }
    }
    return L;
}


int occorrenze_pezzo(lista L, int i) {
    int utilizzotot = 0;
    lista curr = L;

    while(curr != NULL){
        if(curr->pezzi[i]){
            utilizzotot++;
        }
        curr = curr->next;
    }
    return utilizzotot;
}


lista aggiungi_pezzo(lista L, char d[], int i){
    lista curr = L;

    while(curr != NULL){
        if(strcmp(curr->descrizione, d) == 0){
            curr->pezzi[i] = true;
        }
        curr = curr->next;
    }
    return L;
}


class CartaPrepagata{
protected:
    double budget;

public:
    CartaPrepagata(double b){
        budget = b;
    }
    void versamento(double cifra_da_versare){
        if(cifra_da_versare > 0){
            budget +=cifra_da_versare;
        }
    }
    bool pagamento_online(double cifra_del_pagamento){
        if(cifra_del_pagamento < 0){
            return false;
        }else if(cifra_del_pagamento > budget){
            return false;
        }else{
            budget -= cifra_del_pagamento;
            return true;
        }
    }
};


class CartaDeposito : public CartaPrepagata{
protected:
    double deposito;
    double costo_di_prelievo;
    double percentuale;

public:
    CartaDeposito(double d, double cp, double p, double b) : CartaPrepagata(b){
        deposito = d;
        costo_di_prelievo = cp;
        percentuale = p;
    }
    void versamento(double cifra){
        if(cifra < 0){
            return;
        }else{
            double al_deposito = cifra * (percentuale/100);
            double al_budget = cifra - al_deposito;

            CartaPrepagata::versamento(al_budget);
            deposito += al_deposito;
        }
    }
    bool prelievo(double cifra_da_prelevare){
        if(cifra_da_prelevare < 0){
            return false;
        }
        double totale = cifra_da_prelevare + costo_di_prelievo;
        if(totale > deposito){
            return false;
        }else{
            deposito -= totale;
            return true;
        }
    }
};