#include <iostream>
using namespace std;

//versione ricorsiva 
bool dup(int A[], int n, int j, int l){
    if(j >= l){
        return false;
    }else if(A[j] == n){
        return true;
    }else{
        return dup(A, n, j+1, l);
    }
}

bool nodup(int A[], int j, int l){
    if(j >= l){
        return true;
    }else if(dup(A, A[j], j+1, l)){
        return false;
    }else{
        return(nodup(A, j+1, l));
    }
}


//versione iterativa
bool nodup(int A[], int l){
    for(int i=0; i<l; i++){
        for(int j=i+1; j<l; j++){
            if(A[i] == A[j]){
                return false; //duplicato trovato
            }
        }
    }
    return true;
}


struct Alberob{
    int val;
    Alberob* ltree;
    Alberob* rtree;
};
typedef Alberob * btree;

void insert(btree &T, int n){
    if(T == NULL){
        T = new Alberob;
        T->val = n;
        T->ltree = NULL;
        T->rtree = NULL;
    }else if(T->val < n){
        insert(T->rtree, n);
    }else{
        insert(T->ltree, n);
    }
}


void remove_odd(btree &T){
    if(T == NULL){
        return;
    }
    if(T->ltree == NULL && T->rtree == NULL){ //un nodo, per essere foglia, non deve avere figli
        if(T->val % 2 != 0){
            delete T;
            T = NULL;
        }
        return; //molto importante per evitare che la ricorsione proceda su un puntatore che è stato impostato a NULL
    }

    remove_odd(T->ltree);
    remove_odd(T->rtree);
}


class orologio{
    protected:
      int ore;
      int minuti;
      int secondi;

    public:
    bool valid(int o, int m, int s){
        return ((o >= 0 && o < 24) && (m >= 0 && m < 60) && (s >= 0 && s < 60));
    }

    orologio(int o = 0, int m = 0, int s = 0){
        if(valid(o, m, s)){
            ore = o;
            minuti = m;
            secondi = s;
        }else{
            ore = minuti = secondi = 0;
        }
    }
    void impostare(int o, int m, int s){ //mostrare l'ora
        if(!valid(o, m, s)){
            return;
        }else{
            ore = o;
            minuti = m;
            secondi = s;
        }
    }  
    void tick(){ //incrementare l'ora di un secondo
        secondi++;
        if(secondi == 60){
            secondi = 0;
            minuti++;
            if(minuti == 60){
                minuti = 0;
                ore++;
                if(ore == 24){
                    ore = 0;
                }
            }
        }
    }
    int secondiDaMezzanotte(){ //restituisce li numero di secondi passati dalla mezzanotte
        return((ore * 3600)+(minuti * 60)+secondi);
    }
};

class orologioConDoppioFormato : public orologio{
    public:
      orologioConDoppioFormato(int o = 0, int m = 0, int s = 0) : orologio(o, m, s) {}
      
      void stampa24h(){
        cout<< ore << ":" << minuti << ":" << secondi << endl;
      }
      void stampa12h(){
        int ore12 = ore % 12; //comverte l'ora nel formato 12 ore
        if(ore12 == 0){
            ore12 = 12; // Gestisce l'ora 0 come 12 nel formato 12h
        }
        cout<< ore12 << ":" << minuti << ":" << secondi << endl;
    }
};
