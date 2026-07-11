#include <iostream>
using namespace std;

#define DIM 50
#define MAX_CATEGORIE 10

int dup(int A[], int n, int j, int l){
    if(j >= l){
        return 0;
    }else if(A[j] == n){
        return 1 + dup(A, n, j+1, l);
    }else{
        return dup(A, n, j+1, l);
    }
}

bool is_redundant(int A[], int j, int l){
    if(j >= l){
        return true;
    }else if(dup(A, A[j], 0, l) != 2){
        return false;
    }else{
        return is_redundant(A, j+1, l);
    }
}



struct Pista{
    int codice;
    char difficolta;
    bool aperta;
    Pista *next;
};
typedef Pista * lista;

lista piste_aperte(lista L){
    if(L == NULL){
        return NULL;
    }
    lista curr = L;
    lista prec = NULL;

    while(curr != NULL){
        if(!curr->aperta){
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


void chiudi_pista(lista L, int c){
    while(L != NULL){
        if(L->codice == c){
            L->aperta = false;
            return;
        }
        L = L->next;
    }
}


char ritorna_difficolta(lista L, int c){
    while(L != NULL){
        if(L->codice == c){
            return L->difficolta;
        }
        L = L->next;
    }
    return '\0';
}





struct SpesaGiornaliera{
    char categoria[DIM];
    double somma;
};

struct SpesaPeriodica{
    char categoria[DIM];
    double somma;
    int durata;
};

class Bilancio{
    protected:
     SpesaGiornaliera sg[MAX_CATEGORIE];
     int n_sg;

    public:
     Bilancio(int n=0){
        n_sg = n;
     } 
     void aggiungi_spesa(char categoria[], double importo){
        for(int i=0; i<n_sg; i++){
            if(strcmp(sg[i].categoria, categoria) == 0){
                sg[i].somma += importo;
                return;
            }
        }

        //se categoria non trovata, la aggiungo come nuova
        if(n_sg < MAX_CATEGORIE){
            strcpy(sg[n_sg].categoria, categoria);
            sg[n_sg].somma = importo;
            n_sg++;
        }
     }
     double report_mensile(){
        double tot_giornaliera = 0.0;

        for(int i=0; i<n_sg; i++){
            tot_giornaliera += sg[i].somma;
        }

        double spesaMediaGiornaliera = tot_giornaliera/30.0;

        //azzerare le spese
        for(int i=0; i<MAX_CATEGORIE; i++){
            sg[i].somma = 0.0;
        }

        return spesaMediaGiornaliera;
     }
};


class BilancioSmart : public Bilancio{
    protected:
     SpesaPeriodica sp[MAX_CATEGORIE];
     int n_sp;

    public:
     BilancioSmart(int np=0, int n=0) : Bilancio(n){
        n_sp = np;
     } 
     void aggiungi_spesa(char categoria[], double importo){
        for(int i=0; i<n_sp; i++){
            if(strcmp(sp[i].categoria, categoria) == 0){
                sp[i].somma += importo;
                return;
            }
        }

        //se categoria non trovata, la aggiungo come nuova
        if(n_sp < MAX_CATEGORIE){
            strcpy(sp[n_sp].categoria, categoria);
            sp[n_sp].somma = importo;
            n_sp++;
        }
     }
     double report_mensile(){
        double tot_spese = Bilancio::report_mensile();

        for(int i=0; i<n_sp; i++){
            tot_spese += (sp[i].somma / sp[i].durata);
            sp[i].somma = 0.0; //azzero le spese
        }
        return tot_spese;
     }
};
