#include <iostream>
using namespace std;

#define DIM 50

//SE I NUMERI FOSSERO GIA' SISTEMATI NEGLI INDICI GIUSTI SAREBBE CORRETTO
void ordina(int A[], int l){
    for(int i=0; i<l; i+=2){
        for(int j=i+2; j<l; j+=2){
            if((A[i] % 2 == 0) && (A[j] % 2 == 0) && (A[j] > A[i])){
                int tmp = A[i];
                A[i] = A[j];
                A[j] = tmp;
            } 
        }
    }

    for(int i=1; i<l; i+=2){
        for(int j=i+2; j<l; j+=2){
            if((A[i] % 2 != 0) && (A[j] % 2 != 0) && (A[j] < A[i])){
                int tmp = A[i];
                A[i] = A[j];
                A[j] = tmp;
            }
        }
    }
}



//CODICE CORRETTO
void ordina(int A[], int l) {
    // 1. RIPOSIZIONAMENTO: Portiamo i pari negli indici 0, 2, 4... e i dispari in 1, 3, 5...
    for(int i=0; i<l; i++){
        if((i % 2 == 0) && (A[i] % 2 != 0)){ //Se in una posizione pari c'è un numero dispari
            for(int j=i+1; j<l; j++){
                if(A[j] % 2 == 0){ //Cerchiamo il primo pari disponibile
                    int tmp = A[i];
                    A[i] = A[j];
                    A[j] = tmp;
                    break;
                }
            }
        }
        else if((i % 2 != 0) && (A[i] % 2 == 0)){ //Se in una posizione dispari c'è un numero pari
            for(int j=i+1; j<l; j++){
                if(A[j] % 2 != 0){ //Cerchiamo il primo dispari disponibile
                    int tmp = A[i];
                    A[i] = A[j];
                    A[j] = tmp;
                    break;
                }
            }
        }
    }

    // 2. ORDINAMENTO PARI (Decrescente nelle posizioni 0, 2, 4...)
    for(int i = 0; i < l; i += 2){
        for(int j = i + 2; j < l; j += 2){
            if(A[j] > A[i]){
                int tmp = A[i];
                A[i] = A[j];
                A[j] = tmp;
            }
        }
    }

    // 3. ORDINAMENTO DISPARI (Crescente nelle posizioni 1, 3, 5...)
    for(int i = 1; i < l; i += 2){
        for(int j = i + 2; j < l; j += 2){
            if(A[j] < A[i]){
                int tmp = A[i];
                A[i] = A[j];
                A[j] = tmp;
            }
        }
    }
}



struct Vacanza{
    int giorni;
    double prezzo;
    char tipologia[DIM];
    Vacanza *next;
};
typedef Vacanza * lista;

lista inserisci_ordinata(lista head, lista nuova){ //funzione che ordina la lista in base al prezzo
    double prezzoGiornaliero = nuova->prezzo / nuova->giorni;

    if((head == NULL) || ((head->prezzo/head->giorni) > prezzoGiornaliero)){ //inserimento in testa
        nuova->next = head;
        return nuova;
    }

    lista curr = head;
    while((curr->next != NULL) && ((curr->next->prezzo/curr->next->giorni) <= prezzoGiornaliero)){
        curr = curr->next;
    }
    nuova->next = curr->next;
    curr->next = nuova;
    return head;
}

lista filtraTipologia(lista L, char tipo[]){
    lista listaFiltrata = NULL;

    while(L != NULL){
        if(strcmp(L->tipologia, tipo) == 0){
            lista nuovo = new Vacanza;
            nuovo->giorni = L->giorni;
            nuovo->prezzo = L->prezzo;
            strcpy(nuovo->tipologia, L->tipologia);
            nuovo->next = NULL;

            //inserisce ordinatamente in base al prezzo giornaliero
            listaFiltrata = inserisci_ordinata(listaFiltrata, nuovo);
        }
        L = L->next;
    }
    return listaFiltrata;
}



lista piuEconomica(lista L, int g){
    lista economica = NULL;

    while(L != NULL){
        if(L->giorni == g){
            if((economica == NULL) || (economica->prezzo > L->prezzo)){ //se non ho trovato una vacanza economica, o se il prezzo della vacanza corrente è inferiore a quello della vacanza economica trova
                economica = L;
            }
        }
        L = L->next;
    }
    return economica;
}





class Self{
    protected:
     char rifornimento[DIM]; //benzina o diesel
     double litrib;
     double litrid;
     double litriMax;

    public:
     Self(char r[], double lb, double ld, double lmax){
        strcpy(rifornimento, r);
        litrib = lb;
        litrid = ld;
        litriMax = lmax;
     } 
     bool aggiungi_litri(char tipo[], double litri){
        if(strcmp(tipo, "benzina") == 0){
            if(litri + litrib <= litriMax){
                litrib += litri;
                return true;
            }else{
                return false;
            }
        }else if(strcmp(tipo, "diesel") == 0){
            if(litri + litrid <= litriMax){
                litrid += litri;
                return true;
            }else{
                return false;
            }
        }else{
            return false;
        }
     }
     bool decrementa_litri(char tipo[], double litri){
        if(strcmp(tipo, "benzina") == 0){
            if(litrib - litri >= 0){
                litrib -= litri;
                return true;
            }else{
                return false;
            }
        }else if(strcmp(tipo, "diesel") == 0){
            if(litrid - litri >= 0){
                litrid -= litri;
                return true;
            }else{
                return false;
            }
        }else{
            return false;
        }
     }
};


class Servito : public Self{
    protected:
     double litrim;

    public:
     Servito(double lm, char r[], double lb, double ld, double lmax) : Self(r, lb, ld, lmax){
        litrim = lm;
     }
     bool aggiungi_litri(char tipo[], double litri){
        if(!Self::aggiungi_litri(tipo, litri)){
            if(strcmp(tipo, "metano") == 0){
                if(litri + litrim <= litriMax){
                    litrim += litriMax;
                    return true;
                }else{
                    return false;
                }
            }else{
                return false;
            }
        }else{
            return true;
        }
     }
     bool decrementa_litri(char tipo[], double litri){
        if(!Self::decrementa_litri(tipo, litri)){
            if(strcmp(tipo, "metano") == 0){
                if(litrim - litri >= 0){
                    litrim -= litri;
                    return true;
                }else{
                    return false;
                }
            }else{
                return false;
            }
        }else{
            return true;
        }
     }
};



