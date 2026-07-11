#include <iostream>
using namespace std;

#define DIM 50

struct node{
    double val;
    int left;
    int right;
};

int max(int A, int B){
    if(A > B){
        return A;
    }else{
        return B;
    }
}

int altezza(node A[], int i){
    if(i == -1){ //albero vuoto
        return 0; //un albero vuoto ha altezza zero
    }

    int altezzal = altezza(A, A[i].left);
    int altezzar = altezza(A, A[i].right);

    return 1 + max(altezzal, altezzar);
}

int rightmost(node A[], int i){
    if(i == -1){ //albero vuoto
        return -1; //non esiste il figlio destro
    }

    int curr = i;
    while(A[curr].right != -1){
        curr = A[curr].right;
    }
    return curr;
}

struct Piatto{
    char nome[DIM];
    char tipo[DIM];
    double prezzo;
    Piatto *next;
};
typedef Piatto * lista;

lista ordinata(lista L, double p){
    lista last = NULL;
    lista nuova_lista = NULL;

    while(L != NULL){
        if(L->prezzo > p){
            lista nuovo = new Piatto;
            strcpy(nuovo->nome, L->nome);
            strcpy(nuovo->tipo, L->tipo);
            nuovo->prezzo = L->prezzo;
            nuovo->next = NULL;
            
            if(nuova_lista == NULL){
                nuova_lista = nuovo; //il nuovo nodo è il primo della nuova lista
            }else{
                if(strcmp(nuovo->tipo, "antipasto") == 0){ //aggiungo in testa
                    nuovo->next = nuova_lista;
                    nuova_lista = nuovo;
                }
                else if(strcmp(nuovo->tipo, "primo") == 0){
                    if((last == NULL) || (strcmp(last->tipo, "antipasto") == 0)){
                        last->next = nuovo; //aggiungi dopo l'antipasto
                        last = nuovo;
                    }
                }
                else if(strcmp(nuovo->tipo, "secondo") == 0){
                    if((last == NULL) || (strcmp(last->tipo, "primo") == 0)){
                        last->next = nuovo; //aggiungi dopo il primo
                        last = nuovo;
                    }
                }
                else if(strcmp(nuovo->tipo, "dolce") == 0){
                    if((last == NULL) || (strcmp(last->tipo, "secondo") == 0)){
                        last->next = nuovo; //aggiungi dopo il secondo
                        last = nuovo;
                    }
                }
            }
        }
        L = L->next;
    }
    return nuova_lista;
}


double prezzotot(lista L, char n[]){
    while(L != NULL){
        if(strcmp(L->nome, n) == 0){
            return L->prezzo;
        }
        L = L->next;
    }
    return 0.0;
}



class RCA{
    protected:
     int classe_di_rischio;
     double costo_base;
     double servizi_opzionali[3];
     int n_servizi;

    public:
    RCA(int cdr, double cb, double so[], int n){
        classe_di_rischio = cdr;
        costo_base = cb;
        for(int i=0; i<n; i++){
            servizi_opzionali[i] = so[i];
        }
        n_servizi = n;
    } 
    double costo_servizi(){
        double tot = 0.0;
        for(int i=0; i<n_servizi; i++){
            tot += servizi_opzionali[i];
        }
        return tot;
    }
    bool aggiungi_servizio(double p){
        if(n_servizi < 3){
            servizi_opzionali[n_servizi] = p;
            n_servizi++;
            return true;
        }
        return false;
    }
    double calcola_costo(){
        return classe_di_rischio * costo_base + costo_servizi();
    }
};

class RCAKM : public RCA{
    protected:
     double sconto_perc;
     double km_percorsi;
     double sogliakm;
     double costokm;

    public:
    RCAKM(double sp, double kmp, double skm, double ckm, int cdr, double cb, double so[], int n) : RCA(cdr, cb, so, n){
        sconto_perc = sp;
        km_percorsi = kmp;
        sogliakm = skm;
        costokm = ckm;
    }
    void aggiungi_km(double km){
        km_percorsi += km;
    }
    double calcola_costo(){
        double costo_totale = RCA::calcola_costo();
        
        costo_totale = costo_totale - (costo_totale * sconto_perc / 100.0); //devo applicare lo sconto percentuale

        if(km_percorsi > sogliakm){
            double kmExtra = km_percorsi - sogliakm;
            costo_totale += kmExtra * costokm;
        }
        return costo_totale;
    }
};