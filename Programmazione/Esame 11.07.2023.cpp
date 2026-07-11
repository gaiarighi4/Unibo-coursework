#include <iostream>
using namespace std;

#define DIM 50

int dup(int A[], int n, int j, int l){
    if(j >= l){
        return 0;
    }else if(A[j] == n){
        return 1 + dup(A, n, j+1, l);
    }else{
        return dup(A, n, j+1, l);
    }
}

int dupmax(int A[], int l){
    int maxdup = 0;

    for(int i=0; i<l; i++){
        int ndup = dup(A, A[i], 0, l);
        if(ndup > maxdup){
            maxdup = ndup;
        }
    }
    return maxdup;
}


struct Appunto{
    char testo[DIM];
    int pagine;
    int data;
    Appunto *prec;
    Appunto *next;
};
typedef Appunto * lista;

void rimuovi_appunto(lista& L, int giorno){
    if(L == NULL){
        return;
    }
    lista tmp = L;
    while(tmp != NULL){
        if(tmp->data == giorno){
            if(tmp->prec == NULL){
                L = tmp->next;
            }else{
                tmp->prec->next = tmp->next;
            }
            if(tmp->next != NULL){ //aggiorna il collegamento all'indietro del nodo
                tmp->next->prec = tmp->prec;
            }
        }else{
            tmp = tmp->next;
        }
    }
}

lista inverti_lista(lista L){
    if(L == NULL){
        return NULL;
    }
    lista curr = L;
    lista tmp = NULL;

    while(curr != NULL){
        tmp = curr->prec;
        curr->prec = curr->next;
        curr->next = tmp;

        L = curr; //ogni volta curr è l’ultimo nodo processato; quando il ciclo finisce, curr è l’ex ultimo nodo, quindi L diventa automaticamente la nuova testa
        curr = curr->prec; //avanza 
    }
    return L;
}

void testo(lista L, char* output){
    if(L == NULL){
        return;
    }

    lista curr = L;
    lista max = L;

    while(curr != NULL){
        if(curr->pagine > max->pagine){ //se trova un appunto con più pagine
            max = curr;
        }
        curr = curr->next;
    }
    strcpy(output, max->testo); //copia il testo dell'appunto più lungo trovato
}



struct Slot{
    bool prenotato;
    char codice[DIM];
    char destinazione[DIM];
};

class Aeroporto{
    protected:
     Slot slot[24];
     int n_slot;

    public:
     Aeroporto(Slot s[], int n){
        n_slot = n;
        for(int i=0; i<n_slot; i++){
            slot[i] = s[i];
        }
     }
     void aggiungi_volo(char codice[], char destinazione[], int orario){
        if((orario < 0) || (orario >= n_slot)){
            return;
        }
        if(slot[orario].prenotato){
            return;
        }else{
            slot[orario].prenotato = true;
            strcpy(slot[orario].codice, codice);
            strcpy(slot[orario].destinazione, destinazione);
        }

     }
     void rimuovi_volo(char codice[]){
        for(int i=0; i<n_slot; i++){
            if((slot[i].prenotato) && (strcmp(slot[i].codice, codice) == 0)){
                slot[i].prenotato = false;
                return;
            }
        }
     }
};

class AeroportoPlus : public Aeroporto{
    public: 
     AeroportoPlus(Slot s[], int n) : Aeroporto(s, n){}
     void aggiungi_volo(char codice[], char destinazione[], int orario){
        if(codice[0] == 'h'){
            if((orario < 0) || (orario >= n_slot)){
            return;
            }
            if(slot[orario].prenotato){
                return;
            }else{
                slot[orario].prenotato = true;
                strcpy(slot[orario].codice, codice);
                strcpy(slot[orario].destinazione, destinazione);
            }
        }else{
            Aeroporto::aggiungi_volo(codice, destinazione, orario);
        }
     }
     void rimuovi_volo(char codice[]){
        Aeroporto::rimuovi_volo(codice);
     }
};