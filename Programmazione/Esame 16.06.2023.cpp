#include <iostream>
using namespace std;

#define DIM 50

int nocc(int A[], int n, int j, int l){
    if(j >= l){
        return 0;
    }else if(A[j] == n){
        return 1 + nocc(A, n, j+1, l);
    }else{
        return nocc(A, n, j+1, l);
    }
}

int occmagg(int A[], int l){
    int maxocc = 0;

    for(int i=0; i<l; i++){
        int occ = nocc(A, A[i], 0, l);
        if(occ > maxocc){
            maxocc = occ;
        }
    }
    return maxocc;
}



struct Alberob{
    int val;
    Alberob *left;
    Alberob *right;
};
typedef Alberob * albero;

struct Lista{
    int val;
    Lista *next;
};
typedef Lista * lista;

int max(int A, int B){
    if(A > B){
        return A;
    }else{
        return B;
    }
}


void insert_normale(albero& T, int v){
    if(T == NULL){
        T = new Alberob;
        T->val = v;
        T->left = NULL;
        T->right = NULL;
    }else if(v < T->val){
        insert_normale(T->left, v);
    }else{
        insert_normale(T->right, v);
    }
}

void insert_invertito(albero& T, int v){
    if(T == NULL){
        T = new Alberob;
        T->val = v;
        T->left = NULL;
        T->right = NULL;
    }else if(v > T->val){
        insert_invertito(T->left, v);
    }else{
        insert_invertito(T->right, v);
    }
}

// Funzione per creare l'albero binario di ricerca a partire da una lista di interi
void create_tree(albero& T, lista L, bool invertito){
    while(L != NULL){
        if(invertito){
            insert_invertito(T, L->val);
        }else{
            insert_normale(T, L->val);
        }
        L = L->next;
    }
}

albero facimm_ammuina(albero T){
    if(T == NULL){
        return NULL;
    }
    albero tmp = T->left;
    T->left = T->right;
    T->right = tmp;

    facimm_ammuina(T->left);
    facimm_ammuina(T->right);

    return T;
}

int max_depth(albero T){
    if(T == NULL){
        return -1;
    }
    int ld = max_depth(T->left);
    int rd = max_depth(T->right);

    return 1 + max(ld, rd);
}





struct PuntoDiInteresse{
    int identificativo;
    double prezzo;
    char nome[DIM];
};

class Agenzia{
protected:
    double sconto_perc;
    PuntoDiInteresse catalogo[DIM];
    int n_punti;

public:
    Agenzia(double s, int n, PuntoDiInteresse cat[]){
        int i;
        sconto_perc = s;
        n_punti = n;
        for(i=0; i<n_punti; i++){
            catalogo[i] = cat[i];
        }
    }
    double trova_prezzo(int id){
        for(int i=0; i < n_punti; i++){
            if(catalogo[i].identificativo == id){
                return catalogo[i].prezzo;
            }
        }
        return -1.0;
    }

    double calcola_prezzo(int scelti[], int num_scelti){
        double prezzo_tot = 0.0;
        for(int i = 0; i < num_scelti; i++){
            double prezzo = trova_prezzo(scelti[i]); //restituisce il prezzo del punto di interesse associato a quell'identificativo
            if(prezzo != -1.0){
                prezzo_tot += prezzo;
            }
        }

        //int scaglioni = num_scelti / 3;  // Ogni 3 punti, uno sconto
        //double sconto = scaglioni * sconto_perc;

        // Applica lo sconto sul prezzo totale
        //return prezzo_tot - (prezzo_tot * sconto / 100.0);
        return prezzo_tot - (prezzo_tot * ((num_scelti/3)*sconto_perc) / 100.0);
    }
};

class AgenziaVIP : public Agenzia{
protected:
    double salta_coda;
    double guida_turistica;

public:
    AgenziaVIP(double sc, double gt, double s, int n, PuntoDiInteresse cat[]) : Agenzia(s, n, cat){
        salta_coda = sc;
        guida_turistica = gt;
    }
    double calcola_prezzo(int scelti[], int num_scelti){
        double prezzo_totale = Agenzia::calcola_prezzo(scelti, num_scelti);  //prezzo senza i servizi aggiuntivi

        prezzo_totale += salta_coda;  //costo del servizio "salta coda" (una sola volta)
        prezzo_totale += guida_turistica * num_scelti;  //costo del servizio "guida turistica" per ogni punto scelto

        return prezzo_totale;
    }
};