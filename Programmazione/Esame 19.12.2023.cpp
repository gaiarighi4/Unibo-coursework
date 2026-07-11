#include <iostream>
using namespace std;

#define DIM 50
#define N 30
#define M 60

struct Nodo{
    int val;
    int left;
    int right;
};

int somma(Nodo A[], int i=0){
    int tot = A[i].val;

    if(i == -1){
        return 0;
    }
    if(A[i].left != -1){
        tot += somma(A, A[i].left);
    }
    if(A[i].right != -1){
        tot += somma(A, A[i].right);
    }
    return tot;
}

void all_odd(Nodo A[], int i=0){
    if(A[i].val %2 == 0){
        A[i].val++;
    }
    if(A[i].left != -1){
        all_odd(A, A[i].left);
    }
    if(A[i].right != -1){
        all_odd(A, A[i].right);
    }
}


struct Esame{
    char nome[DIM];
    int cfu;
    int voto;
    Esame *next;
};
typedef Esame * lista;

lista rifiuta_esame(lista L, int cfu){
    if(L == NULL){
        return NULL;
    }
    lista prec = NULL;
    lista curr = L;

    while(curr != NULL){
        if(curr->cfu == cfu){
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

void min_esame(lista L, char nome[]){
    if(L == NULL){
        return;
    }
    lista min = L;
    lista curr = L;

    while(curr != NULL){
        if(curr->voto < min->voto){
            min = curr;
        }
        curr = curr->next;
    }
    strcpy(nome, min->nome);
}

double media(lista L){
    if(L == NULL){
        return 0.0;
    }
    int totcfu = 0;
    double totvoto = 0.0;

    while(L != NULL){
        totvoto += (L->voto * L->cfu);
        totcfu += L->cfu;

        L = L->next;
    }
    if(totcfu > 0){
        return totvoto / totcfu;
    }else{
        return 0.0;
    }
}



struct Camera{
    int id;
    int letti;
    bool disponibile;
};

struct Ombrellone{
    int id;
    bool disponibile;
};


class Albergo{
    protected:
     Camera camere[N];

    public:
     Albergo(Camera cam[]){
        for(int i=0; i<N; i++){
            camere[i] = cam[i];
        }
     } 
     int prenota(int letti){
        for(int i=0; i<N; i++){
            if(camere[i].disponibile && camere[i].letti == letti){
                camere[i].disponibile = false;
                return camere[i].id;
            }
        }
        return -1;
     }
};     

class AlbergoConSpiaggia : public Albergo{
    protected:
     Ombrellone ombrelloni[M];
    
    public:
    AlbergoConSpiaggia(Ombrellone omb[], Camera cam[]) : Albergo(cam){
        for(int i=0; i<M; i++){
            ombrelloni[i] = omb[i];
        }
    }
    int prenota_ombrellone(){
        for(int i=0; i<M; i++){
            if(ombrelloni[i].disponibile ){
                ombrelloni[i].disponibile = false;
                return ombrelloni[i].id;
            }
        }
        return -1;
    }
    int prenota(int letti, bool& buon_fine){
        int id_camera = Albergo::prenota(letti);

        if(id_camera != -1){
            buon_fine = true;
            int id_ombrellone = prenota_ombrellone();

            if(id_ombrellone != -1){
                cout << "Camera " << id_camera << " e ombrellone " << id_ombrellone << " prenotati con successo." << endl;
            }else{
                cout << "Camera " << id_camera << " prenotata con successo, ma nessun ombrellone disponibile." << endl;
            }
            return id_camera;

        }else{
            buon_fine = false;
            cout << "Nessuna camera disponibile con " << letti << " letti." << endl;
            return -1;
        }
    }
};