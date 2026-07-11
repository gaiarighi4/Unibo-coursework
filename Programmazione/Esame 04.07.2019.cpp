#include <iostream>
using namespace std;

#define DIM 100

int norma(int A[], int l){
    int pos = 0;
    int neg = 0;

    for(int i=0; i<l; i++){
        if(A[i] > 0){
            pos += A[i];
        }else{
            neg += abs(A[i]);
        }
    }
    return pos - neg;
}


struct Alberot{
    int val;
    Alberot* ltree;
    Alberot* ctree;
    Alberot* rtree;
};
typedef Alberot * alberot;

void ammuina(alberot T){
    if(T == NULL){
        return;
    }else if(T->val % 2 == 0){
        alberot tmp = T->ltree;
        T->ltree = T->ctree;
        T->ctree = T->rtree;
        T->rtree = tmp;
    }else{
        alberot tmp = T->ltree;
        T->ltree = T->rtree;
        T->rtree = T->ctree;
        T->ctree = tmp;
    }
    ammuina(T->ltree);
    ammuina(T->ctree);
    ammuina(T->rtree);
}

void upgrade10(alberot T){
    if(T == NULL){
        return;
    }
    upgrade10(T->ltree);
    upgrade10(T->ctree);
    upgrade10(T->rtree);

    if((T->ltree == NULL) && (T->ctree == NULL) && (T->rtree == NULL)){
        if(T->val < -10){
            delete T;
            T = NULL;
        }else{
            T->val += 10;
        }
    }
}


struct Ospite{
    char nome[10];
    int omb_affittati;
    int sdra_affittate;
};

class Stabilimento{
    protected:
     int ombrelloni;
     int sdraio;
     Ospite ospiti[DIM];
     int num_ospiti;

    public:
     Stabilimento(int o, int s, int n){
        ombrelloni = o;
        sdraio = s;
        num_ospiti = n;
     } 
     bool insert(char nome[], int ombrelloni_rich, int sdraio_rich){
        if((num_ospiti < 100) && (ombrelloni_rich <= ombrelloni) && (sdraio_rich <= sdraio)){
            strcpy(ospiti[num_ospiti].nome, nome);
            ospiti[num_ospiti].omb_affittati = ombrelloni_rich;
            ospiti[num_ospiti].sdra_affittate = sdraio_rich;

            ombrelloni -= ombrelloni_rich;
            sdraio -= sdraio_rich;
            num_ospiti++;

            return true;
        }
        return false;
     }
     bool remove(char nome[]){
        for(int i=0; i<100; i++){
            if(strcmp(ospiti[i].nome, nome) == 0){
                num_ospiti--;
                ombrelloni += ospiti[i].omb_affittati;
                sdraio += ospiti[i].sdra_affittate;

                return true;
            }
        }
        return false;
     }
};

class Stabilimento_plus : public Stabilimento{
    protected:
     double costo_ombrelloni;
     double costo_sdraio;

    public:
     Stabilimento_plus(double co, double cs, int o, int s, int n) : Stabilimento(o, s, n){
        costo_ombrelloni = co;
        costo_sdraio = cs;
     }
     double guadagno(){
        double guadagnotot = 0.0;

        for(int i=0; i<num_ospiti; i++){
            guadagnotot += (ospiti[i].omb_affittati * costo_ombrelloni) + (ospiti[i].sdra_affittate * costo_sdraio);
        }
        return guadagnotot;
     }
};