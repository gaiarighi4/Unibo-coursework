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


struct Articolo{
    char titolo [DIM];
    int id;
    bool accettato;
    Articolo *next;
};
typedef Articolo * lista;

lista inserisci_articolo(lista L, char titolo[]){
    lista nuovo = new Articolo;
    strcpy(nuovo->titolo, titolo);
    nuovo->accettato = false;
    nuovo->next = NULL;

    if(L == NULL){
        nuovo->id = 1;
        return nuovo;
    }

    lista curr = L;
    while(curr->next != NULL){
        curr = curr->next;
    }
    curr->next = nuovo;
    nuovo->id = curr->id +1;

    return L;
}

void rifiuta_articolo(lista L, char titolo[]){
    if(L == NULL){
        return;
    }
    while(L != NULL){
        if(strcmp(L->titolo, titolo) == 0){
            L->accettato = false;
        }
        L = L->next;
    }
}

double acceptance_rate(lista L){
    if(L == NULL){
        return 0.0;
    }
    double tot_articoli = 0.0;
    double articoli_accettati = 0.0;

    while(L != NULL){
        tot_articoli++;
        if(L->accettato){
            articoli_accettati++; 
        }
        L = L->next;
    }
    if(tot_articoli == 0){
        return 0.0;
    }else{
        return (articoli_accettati/tot_articoli)*100;
    }
}


class Campo{
    protected:
     bool orari[24];
     double costo;

    public:
     Campo(double co){
        for(int i=0; i<24; i++){
            orari[i] = false;
        }
        costo = co;
     } 
     bool prenota_campo(int ora){
        if((ora < 0) || (ora >= 24)){
            return false;
        }else if(orari[ora]){ //campo già prenotato
            return false;
        }else{
            orari[ora] = true;
            return true;
        }
     }
     double calcola_ricavi(){
        int n_prenotazioni = 0;

        for(int i=0; i<24; i++){
            if(orari[i]){
                n_prenotazioni++;
            }
        }
        return n_prenotazioni * costo;
     }
};


class CampoNoleggio : public Campo{
    protected:
     int racchette[24];
     double costo_racchetta;

    public:
     CampoNoleggio(double cr, double co) : Campo(co){
        for(int i=0; i<24; i++){
            racchette[i] = 0;
        }
        costo_racchetta = cr;
     }
     bool prenota_campo_attrezzature(int ora, int n_racchette){
        if((ora < 0) || (ora >= 24)){
            return false;
        }else if(orari[ora]){
            return false;
        }else{
            orari[ora] = true;
            racchette[ora] = n_racchette;
            return true;
        }
     }
     int totale_prenotazioni(){
        int racchette_tot = 0;

        for(int i=0; i<24; i++){
            racchette_tot += racchette[i];
        }
        return racchette_tot;
     }
     double calcola_ricavi(){
        double prenotazione_campi = Campo::calcola_ricavi();

        return prenotazione_campi + (totale_prenotazioni() * costo_racchetta);
     }
};