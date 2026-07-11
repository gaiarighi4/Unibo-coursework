#include <iostream>
using namespace std;

#define DIM 50

bool dup(int A[], int n, int j, int l){
    if(j >= l){
        return false;
    }else if(A[j] == n){
        return true;
    }else{
        return dup(A, n, j+1, l);
    }
}

bool contiene(int A[], int j, int l){
    if(j >= l){
        return false;
    }else if(dup(A, A[j], j+1, l)){
        return true;
    }else{
        return contiene(A, j+1, l);
    }
}


struct Aeroporto{
    char partenza[DIM];
    char arrivo[DIM];
    double prezzo;
    int posti_liberi;
    Aeroporto *next;
};
typedef Aeroporto * lista;

lista aggiungi_volo(lista L, char p[], char a[], double costo, int pl){
    lista T = new Aeroporto;
    strcpy(T->partenza, p);
    strcpy(T->arrivo, a);
    T->prezzo = costo;
    T->posti_liberi = pl;
    T->next = NULL;

    if(L == NULL){ //lista vuota
        return T;
    }
    if(L->prezzo > costo){ //inserimento in testa
        T->next = L;
        return T;
    }else{ //inserimento nel primo posto utile
        lista tmp = L;
        while((tmp->next != NULL) && (tmp->next->prezzo < costo)){
            tmp = tmp->next;
        }
        //passi per agganciare il nuovo nodo alla lista
        T->next = tmp->next;
        tmp->next = T;
    }
    return L;
}

bool tratta(lista L, char p[], char a[]){
    while(L != NULL){
        if((strcmp(L->partenza, p) == 0) && (strcmp(L->arrivo, a) == 0)){
            return true;
        }
        L = L->next;
    }
    return false;
}

double calcola_prezzo(lista L, char p[], char a[], int biglietti){
    double prezzo_tot = 0.0;

    while(L != NULL){
        if((strcmp(L->partenza, p) == 0) && (strcmp(L->arrivo, a) == 0)){
            if(L->posti_liberi >= biglietti){ //condizione da controllare dopo aver visto se esiste la tratta
                prezzo_tot += L->prezzo * biglietti;
                L->posti_liberi -= biglietti;
                return prezzo_tot;
            }else{
                return -1; //non ci sono posti liberi
            }
        }
        L = L->next;
    }
    return -1; //volo non trovato
}


class BigliettoUrbano{
    protected:
     double prezzo;

    public:
     BigliettoUrbano(double p){
        prezzo = p;
     }
     double calcola_prezzo(){
        return prezzo;
     }

};

class BigliettoExtraUrbano : public BigliettoUrbano{
    protected: 
     double prezzo_km;
     double distanza_km;

    public:
     BigliettoExtraUrbano(double pkm, double dkm,double p) : BigliettoUrbano(p){
        prezzo_km = pkm;
        distanza_km = dkm;
     }
     double calcola_prezzo(){
        return BigliettoUrbano::calcola_prezzo() + (prezzo_km * distanza_km);
     }
     double calcola_distanza(){
        return distanza_km;
     }
};

class BigliettoNazionale : public BigliettoExtraUrbano{
    protected:
     double prezzo_km_av;
     double km_extra;

    public:
     BigliettoNazionale(double pav, double kme, double pkm, double dkm,double p) : BigliettoExtraUrbano(pkm, dkm, p){
        prezzo_km_av = pav;
        km_extra = kme;
     }
     double calcola_prezzo(){
        return BigliettoExtraUrbano::calcola_prezzo() + (prezzo_km_av * km_extra);
     }
     double calcola_distanza(){
        return BigliettoExtraUrbano::calcola_distanza() + km_extra;
     }

};

