#include <iostream>
using namespace std;

#define DIM 50

struct Elem{
    int val;
    int next;
};

struct List{
    int init;  //indice del primo elemento della lista
    Elem vect[DIM];
};

int last_index(List l, int length){
    if(l.init == -1){ //lista vuota
        return -1;
    }
    int i=0;
    int curr = l.init;
    while(l.vect[curr].next != -1 && i < length){
        curr = l.vect[curr].next;
        i++;
    }
    if(i == length){
        return -1;
    }
    return curr;
}

int get_min(List l, int length) {
    if(l.init == -1){
        return -1;
    }
    int curr = l.init;
    int i = 0;
    int min = l.vect[curr].val;

    while(l.vect[curr].next != -1 && i < length){
        if(l.vect[curr].val < min){
            min = l.vect[curr].val;
        }
        curr = l.vect[curr].next;
        i++;
    }
    return min;
}


struct Prodotto{
    char nome[DIM];
    int quantita;
    double prezzo;
    Prodotto *next;
};
typedef Prodotto * lista;


lista rimuovi_quantita(lista L, char nome[]){
    if(L == NULL){
        return NULL;
    }
    //caso testa
    if(strcmp(L->nome, nome) == 0){
        L->quantita -= 1;
        if(L->quantita == 0){
            lista tmp = L->next;
            delete L;
            return tmp;
        }
    }

    //scorro la lista per trovare il nodo da rimuovere
    lista curr = L;
    while(curr->next != NULL){
        if(strcmp(curr->next->nome, nome) == 0){
            curr->next->quantita -= 1;
            if(curr->next->quantita == 0){
                lista tmp = curr->next;
                curr->next = curr->next->next;
                delete tmp;
            }
            return L;
        }
        curr = curr->next;
    }
    return L;
}


//altra versione
lista rimuovi_quantita(lista L, char n[]){
    if(L == NULL){
        return NULL;
    }
    lista curr = L;
    lista prev = NULL;

    while(curr != NULL){
        if(strcmp(curr->nome, n) == 0){
            curr->quantita -= 1;

            // Se la quantità diventa 0, rimuovo il nodo
            if(curr->quantita == 0){
                if(prev == NULL){
                    L = curr->next;
                }else{
                    prev->next = curr->next;
                }
                delete curr;
                return L;
            }
            // Se la quantità non è 0, esco dalla funzione
            return L;
        }
        prev = curr;
        curr = curr->next;
    }
    return L; //se non trovo il prodotto, restituisco la lista
}


double valore_magazzino(lista L){
    if(L == NULL){
        return 0.0;
    }
    double valore_tot = 0.0;
    while(L != NULL){
        valore_tot += L->quantita * L->prezzo;
        L = L->next;
    }
    return valore_tot;
}


char* nome_prodotto(lista L){
    if(L == NULL){
        return NULL;
    }
    lista maggiore_quantita = L;
    while(L != NULL){
        if(L->quantita > maggiore_quantita->quantita){
            maggiore_quantita = L;
        }
        L = L->next;
    }
    return maggiore_quantita->nome;
}


struct PostoAuto{
    char targa[DIM];
    int ora_inizio;
    bool libero;
};

class Parcheggio{
protected:
    double prezzo;
    PostoAuto posti_auto[DIM];
    int num_posti;

public:
    Parcheggio(double p, PostoAuto pa[]){
        int i;
        prezzo = p;
        for(i = 0; i < num_posti; ++i){ 
            posti_auto[i] = pa[i];
        }
    }

    bool occupa_posto(char targa[], int inizio){
        for(int i = 0; i < num_posti; ++i){
            if(posti_auto[i].libero){ 
                strcpy(posti_auto[i].targa, targa);
                posti_auto[i].ora_inizio = inizio;
                posti_auto[i].libero = false;
                return true;
            }
        }
        return false; // Nessun posto libero
    }

    double libera_posto(char targa[], int fine){
        for(int i = 0; i < num_posti; ++i){
            if((!posti_auto[i].libero) && (strcmp(posti_auto[i].targa, targa) == 0)){
                //calcola il costo del parcheggio
                int durata = fine - posti_auto[i].ora_inizio;
                if(durata < 0){
                    return -1;
                }
                double costo = durata * prezzo;

                // Liberiamo il posto
                posti_auto[i].libero = true;
                strcpy(posti_auto[i].targa, ""); //svuota la stringa
                posti_auto[i].ora_inizio = -1;

                return costo;
            }
        }
        return -1; //targa non trovata
    }
};


class ParcheggioConOrari : public Parcheggio{
protected:
    int ora_inizio_pagamento;
    int ora_fine_pagamento;

public:
    ParcheggioConOrari(int ip, int fp, double p, PostoAuto pa[]) : Parcheggio(p, pa){
        ora_inizio_pagamento = ip;
        ora_fine_pagamento = fp;
    }

    bool occupa_posto(char targa[], int inizio){
        if(inizio < ora_inizio_pagamento || inizio >= ora_fine_pagamento){
            return false;
        }
        return Parcheggio::occupa_posto(targa, inizio);
    }

    double libera_posto(char targa[], int fine){
        if(fine <= ora_inizio_pagamento || fine > ora_fine_pagamento){
            return -1;  // L'ora di fine è fuori dall'intervallo di pagamento
        }
        return Parcheggio::libera_posto(targa, fine);
    }
};



