#include <iostream>
using namespace std;

#define DIM 100

int nocc(int A[], int n, int j, int l){
    if(j >= l){
        return 0;
    }else if(A[j] == n){
        return 1 + nocc(A, n, j+1, l);
    }else{
        return nocc(A, n, j+1, l);
    }
}

int occdx(int A[], int l){
    int minocc = l+1;
    int res = -1;

    for(int i=l-1; i>=0; i--){
        int occ = nocc(A, A[i], 0, l);
        if(occ < minocc){
            minocc = occ;
            res = A[i];
        }
    }
    return res;
}



struct Impegno{
    double inizio;
    double fine;
    char descrizione[DIM];
    Impegno *next;
};
typedef Impegno * lista;

lista attivita_brevi(lista L){
    lista brevi = NULL;

    while(L != NULL){
        if(L->fine - L->inizio <= 1.0){
            lista nuovo = new Impegno;
            nuovo->inizio = L->inizio;
            nuovo->fine = L->fine;
            strcpy(nuovo->descrizione, L->descrizione);
            nuovo->next = NULL;

            if((brevi == NULL) || (brevi->inizio > nuovo->inizio)){ //inserimento in testa
                nuovo->next = brevi;
                brevi = nuovo;
            }else{
                lista tmp = brevi;
                while(tmp->next != NULL && tmp->next->inizio < nuovo->inizio){
                    tmp = tmp->next;
                }
                nuovo->next = tmp->next;
                tmp->next = nuovo;
            }
        }
        L = L->next;
    }
    return brevi;
}

int attivita_fuori_orario(lista L){
    int attivita = 0;

    while(L != NULL){
        if(L->inizio < 9.0 || L->fine > 17.0){
            attivita++;
        }
        L = L->next;
    }
    return attivita;
}

double inizio_attivita(lista L, char nome[]){
    while(L != NULL){
        if(strcmp(L->descrizione, nome) == 0){
            return L->inizio;
        }
        L = L->next;
    }
    return -1.0;
}




struct Camera{
    int id;
    int letti_singoli;
    int letti_matrimoniali;
    bool libera;
};

struct Consumazione{
    int id_camera;
    int tot_consumazioni;
};


class Albergo{
    protected:
     Camera camere[DIM];
     int n_camere;
     double costo;

    public:
     Albergo(Camera cam[], int n, double c){
        n_camere = n;
        for(int i=0; i<n; i++){
            camere[i] = cam[i];
        }
        costo = c;
     }
     bool prenota_camera(int nls, int nlm){
        for(int i=0; i<n_camere; i++){
            if(camere[i].libera && camere[i].letti_singoli >= nls && camere[i].letti_matrimoniali >= nlm){
                camere[i].libera = false;
                return true;
            }
        }
        return false;
     }
     double check_out(int id){
        for(int i=0; i<n_camere; i++){
            if(camere[i].id == id){
                double costo_tot = (camere[i].letti_singoli * costo) + (camere[i].letti_matrimoniali * costo * 2);
                camere[i].libera = true;
                return costo_tot;
            }
        }
        return -1.0;
     }
};


class AlbergoRistorante : public Albergo{
    protected: 
     Consumazione consumazioni[DIM];
     int n_consumazioni;
    
    public:
    AlbergoRistorante(Consumazione con[], int nc, Camera cam[], int n, double c) : Albergo(cam, n, c){
        n_consumazioni = nc;
        for(int i=0; i<nc; i++){
            consumazioni[i] = con[i];
        }
    }
    void aggiungi_pasto(int id_camera, double costoc){
        for(int i=0; i<n_consumazioni; i++){
            if(consumazioni[i].id_camera == id_camera){
                consumazioni[i].tot_consumazioni += costoc;
                return;
            }
        }
        consumazioni[n_consumazioni].id_camera = id_camera;
        consumazioni[n_consumazioni].tot_consumazioni = costoc;
        n_consumazioni++;
    }
    double check_out(int id_camera){
        double tot = Albergo::check_out(id_camera);

        for(int i=0; i<n_consumazioni; i++){
            if(consumazioni[i].id_camera == id_camera){
                tot += consumazioni[i].tot_consumazioni;
            }
        }
        return tot;
    }
};