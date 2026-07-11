#include <iostream>
using namespace std;

#define DIM 50
#define MAX_INCONTRI 10 


// NOTA: LE REGION MARCATE DEBUG SONO PER 
// TESTARE IL CODICE NON SONO NECESSARIE NEL COMPITO
// REGION DEBUG 
//#include <bits/stdc++.h> 

struct nodo {
    int val;
    int next;
};

void swap(int *p, int *d) {
    int tmp = *p; 
    *p = *d; 
    *d = tmp; 
}
// ENDREGION DEBUG

// REGION ESERCIZIO 1

int i_revert(nodo arr[], int lun, bool *noswap, int j=0) {
  if(arr[j].next == -1) {
    swap(&arr[0].val, &arr[j].val);
    return arr[0].next;
  } else {
    int index = i_revert(arr, lun, noswap, arr[j].next);
    if(arr[j].next == index || index == j) *noswap = true;
    if(!(*noswap)) {
      swap(&arr[j].val, &arr[index].val);
      return arr[index].next;
    }
    return 0;
  }
}

// La funzione da chiamare Ã¨ revert, che internamente chiama la funzione ricorsiva i_revert
void revert(nodo arr[], int lun) {
  bool swap = false;
  i_revert(arr, lun, &swap);
}






struct nodo{
    int val;
    int next;
};

int inverti(nodo A[], int curr, int prev){
    if(curr == -1){
        return prev;
    }
    int next_node = A[curr].next;

    A[curr].next = prev;

    inverti(A, next_node, curr);
}





struct Viaggio{
    char spartenza[DIM];
    char sarrivo[DIM];
    double prezzo;
    int posti_disponibili;
    int cambi;
    Viaggio *next;
};
typedef Viaggio * lista;

double cerca_viaggio(lista L, char partenza[], char arrivo[], int posti, int maxcambi){
    while( L != NULL){
        if((strcmp(L->spartenza, partenza) == 0) && (strcmp(L->sarrivo, arrivo) == 0)){
            if((L->posti_disponibili >= posti) && (L->cambi <= maxcambi)){
                return L->prezzo * posti;
            }
        }
        L = L->next;
    }
    return -1.0;
}

void aggiungi_viaggio(lista L, char partenza[], char arrivo[], double p, int posti, int c){
    lista tmp = L;
    while(tmp != NULL){
        if((strcmp(L->spartenza, partenza) == 0) && (strcmp(L->sarrivo, arrivo) == 0)){
            return;
        }
        tmp = tmp->next;
    }

    lista nuovo = new Viaggio;
    strcpy(nuovo->spartenza, partenza);
    strcpy(nuovo->sarrivo, arrivo);
    nuovo->prezzo = p;
    nuovo->posti_disponibili = p;
    nuovo->cambi = c;
    nuovo->next = NULL;

    if(L == NULL){
        L = nuovo;
    }else{
        lista curr = L;
        while(curr->next != NULL){
            curr = curr->next;
        }
        curr->next = nuovo;
    }
}



struct Incontro{
    double orario;
    char titolo[DIM];
    char nome_relatore[DIM];
};

class Conferenza{
    protected:
     double inizio;
     double fine;
     double pausa;
     Incontro incontri[MAX_INCONTRI];
     int n_incontri;

    public:
    Conferenza(double i, double f, double p, int n=0){
        inizio = i;
        fine = f;
        pausa = p;
        n_incontri = n;
    } 
    int slot_disponibili(){
        return MAX_INCONTRI - n_incontri;
    }
    bool controlla_orario(double orario){
        return((orario >= inizio) && (orario < fine));
    }
    bool controlla_slot(double orario){
        for(int i=0; i<n_incontri; i++){
            if(incontri[i].orario == orario){
                return false;
            }
        }
        return true;
    }
    bool aggiungi_incontro(double orario, char titolo[], char relatore[]){
        if(!controlla_orario(orario)){
            return false;
        }
        if(!controlla_slot(orario)){
            return false;
        }

        //aggiungi l'incontro
        incontri[n_incontri].orario = orario;
        strcpy(incontri[n_incontri].titolo, titolo);
        strcpy(incontri[n_incontri].nome_relatore, relatore);
        n_incontri++;
        return true;
    }
};


class ConferenzaPremium : public Conferenza{
    protected:
     double orario_poster;

    public:
     ConferenzaPremium(double op, double i, double f, double p, int n=0) : Conferenza(i, f, p, n){
        orario_poster = op;
     }
     bool controlla_orario(double orario){
        if((orario < inizio) || (orario >= fine)){
            return false;
        }
        if((orario == pausa) || (orario == orario_poster)){
            return false;
        }
        return true;
     }
     bool controlla_slot(double orario){
        if(orario == orario_poster){
            return false;
        }
        return Conferenza::controlla_slot(orario);
     }
};