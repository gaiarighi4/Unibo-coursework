#include <iostream>
using namespace std;

const int length = 100;

struct elem{
    int val;
    int next;
};

struct lista{
    int init;
    elem vect[length];
};

int last_index(lista L){
    if(L.init == -1){ //caso lista vuota
        return -1;
    }    

    bool visited[length] = {false}; //per vedere se ho già visitato quel nodo
    int curr = L.init;

    while(curr != -1){
        if(visited[curr]){ //lista circolare
            return -1;
        }
        visited[curr] = true;

        if(L.vect[curr].next == -1){ //se arrivo alla fine della lista
            return curr;
        }

        curr = L.vect[curr].next;
    }

    return -1;
}

int get_min(lista L){
    bool visited[length] = {false};

    int curr = L.init;
    int minimo = L.vect[curr].val;

    while(true){ //perchè l'uscita dipende da condizioni interne
        if(L.vect[curr].val < minimo){
            minimo = L.vect[curr].val;
        }

        visited[curr] = true;
        int next = L.vect[curr].next;

        if(next == -1 || visited[next]){ //fine lista oppure ciclo
            break;
        }

        curr = next;
    }
    return minimo;
}



struct attivita{
    int nome;
    int durata;
    attivita* next;
};
typedef attivita * plist;

plist inserisci_ordinato(plist L, plist nodo){
    if(L == NULL || nodo->durata < L->durata){ //lista vuota o inserimento in testa
        nodo->next = L;
        return nodo;
    }

    plist curr = L;
    while(curr->next != NULL && curr->next->durata <= nodo->durata){
        curr = curr->next;
    }
    nodo->next = curr->next;
    curr->next = nodo;

    return L;
}

plist aggiungi_attivita(plist L, plist T){ //stacca un nodo alla volta da T e lo inserisce in ordine in L
    while(T != NULL){
        plist temp = T;
        T = T->next;
        temp->next = NULL;
        L = inserisci_ordinato(L, temp);
    }
    return L;
}

plist rimuovi_attivita(plist L, int n){
    if(L == NULL){
        return NULL;
    }
    plist curr = L;
    plist prec = NULL;

    while(curr != NULL){
        if(L->nome == n){
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



struct fermata {
    char nome[20];
    int codice;
};

class Autobus {
protected:
    fermata percorso[10];
    int n_fermate;
    int pos;
    int dir; // 1 avanti, -1 indietro

public:
    Autobus(fermata P[], int n_f) {
        n_fermate = n_f;
        for (int i = 0; i < n_fermate; i++)
            percorso[i] = P[i];
        pos = 0;
        dir = 1;
    }

    int go(){
        if(pos == n_fermate - 1){ //sono all'ultima fermata e devo tornare indietro
            dir = -1;
        }else if(pos == 0){ //sono alla prima fermata
            dir = 1;
        }    
        pos += dir; //spostamento
        return percorso[pos].codice;
    }

    int direzione(){
        if(dir == 1){ //se sto andando avanti
            return percorso[n_fermate - 1].codice; //il capolinea è l'ultima fermata
        }else{
            return percorso[0].codice; //il capolinea è la prima fermata
        }
    }
};


class Autobus_con_corse : public Autobus {
    int corse;

public:
    Autobus_con_corse(int c = 0, fermata P[], int n) : Autobus(P, n){}

    int go(){ //va ridefinito per contare le corse
        int prev = pos;
        int codice = Autobus::go();

        if((prev == 0 && pos == n_fermate - 1) || (prev == n_fermate - 1 && pos == 0)){  //se ero alla prima e arrivo all'ultima o viceversa
            corse++; //ho completato le corse
        }
        return codice;
    }

    int num_corse(){
        return corse;
    }
};
