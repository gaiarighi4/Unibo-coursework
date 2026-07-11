#include <iostream>
using namespace std;

#define DIM 50

void pari_dispari(int A[], int j, int l){
    if(j >= l){
        return;
    }else if(A[j] % 2 == 0){
        pari_dispari(A, j+1, l);
    }else if(A[l] % 2 != 0){
        pari_dispari(A, j, l-1);
    }else{
        int tmp = A[j];
        A[j] = A[l];
        A[l] = tmp;
        pari_dispari(A, j+1, l-1);
    }
}


struct Regalo{
    char nome[DIM];
    double prezzo;
    char dest[DIM];
    Regalo *next;
};
typedef Regalo * lista;

lista inserisci(lista L, char n[], double p, char d[]){
    lista T = new Regalo;
    strcpy(T->nome, n);
    T->prezzo = p;
    strcpy(T->dest, d);
    T->next = L; //regalo aggiunto in testa 
    return T;    
}

lista rimuovi_regalo(lista L, char n[]){
    if(L == NULL){
        return NULL;
    }
    lista curr = L;
    lista prec = NULL;

    while(curr != NULL){
        if(strcmp(curr->nome, n) == 0){
            if(prec == NULL){
                L = curr->next;
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

double costo_totale(lista L, char d[]){
    double tot = 0.0;

    while(L != NULL){
        if(strcmp(L->dest, d) == 0){
            tot += L->prezzo;
        }
        L = L->next;
    }
    return tot;
}


class Automobile{
    protected:
     char modello[DIM];
     double consumo_per_100km;

    public:
     Automobile(char m[], double c){
        strcpy(modello, m);
        consumo_per_100km = c;
     }
     double calcola_consumi(double km){
        if(km < 0.0){
            km = 0.0;
        }
        return consumo_per_100km / 100 * km;
     }
     double calcola_costo(double km, double euro){
        if(euro < 0.0){
            euro = 0.0;
        }
        return calcola_consumi(km) * euro;
     }
};

class Benzina : public Automobile{
    protected:
     double capacita_serbatoio;

    public:
     Benzina(double cs, char m[], double c) : Automobile(m, c){
        capacita_serbatoio = cs;
     }
     double calcola_autonomia(){
        return capacita_serbatoio / consumo_per_100km * 100.0;
     }
};

class Ibrida : public Benzina{
    protected:
     double risparmio; //in percentuale

    public:
     Ibrida(double r, double cs, char m[], double c) : Benzina(cs, m, c){
        risparmio = r;
     }
     double calcola_consumi(double km){
        return (100.0 - risparmio) / 100.0 * Automobile::calcola_consumi(km); //dal 100% tolgo la percentuale di risparmio
    }

    double calcola_costo(double km, double euro){
        return (100.0 - risparmio) / 100.0 * Automobile::calcola_costo(km, euro); //dal 100% tolgo la percentuale di risparmio
    }

    double calcola_autonomia(){
        return 100.0 / (100.0 - risparmio) * Benzina::calcola_autonomia();
    }
};

class Elettrica : public Automobile{
    protected:
     double batteria;

    public:
     Elettrica(double b, char m[], double c) : Automobile(m, c){
        batteria = b;
     }
     double calcola_autonomia(){
        return batteria / consumo_per_100km * 100;
     }   
};