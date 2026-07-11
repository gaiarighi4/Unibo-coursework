#include <iostream>
using namespace std;

#define DIM 50

struct node{
    double val;
    int next;
};

bool dfs(int current, bool visited[], bool stack[], node A[]){
    if(!visited[current]){
        // Marca il nodo come visitato e aggiungilo allo stack
        visited[current] = true;
        stack[current] = true;

        // Segui il nodo successivo
        int nextNode = A[current].next;
        if(nextNode != -1){ // Se esiste un nodo successivo
            if(!visited[nextNode] && dfs(nextNode, visited, stack, A)){
                return true; // Ciclo trovato
            }else if(stack[nextNode]){ // Se il nodo successivo è già nello stack, abbiamo trovato un ciclo
                return true;
            }
        }
    }
    // Rimuovi il nodo dallo stack prima di tornare indietro
    stack[current] = false;
    return false;
}

bool there_are_loops(node A[], int n){
    bool visited[n]; // Array per tenere traccia dei nodi visitati
    bool stack[n];   // Array per tenere traccia dei nodi nello stack

    // Inizializza gli array a false
    for(int i = 0; i < n; i++){
        visited[i] = false;
        stack[i] = false;
    }

    for(int i = 0; i < n; i++){
        if(!visited[i]){ // Se il nodo non è stato visitato, avvia DFS
            if(dfs(i, visited, stack, A)){
                return true; // Se troviamo un ciclo
            }
        }
    }
    return false; // Nessun ciclo trovato
}


struct Appartamento{
    char nome[DIM];
    double prezzo;
    int persone;
    Appartamento *next;
};
typedef Appartamento * lista;

void elimina_economico(lista L, int persone){
    if(L == NULL){
        return;
    }
    lista curr = L;
    lista prec = NULL;
    lista economico = NULL;
    lista prec_economico = NULL;
    double prezzo_minimo = -1.0;

    //scorri la lista per trovare l'appartamento più economico che può ospitare il numero di persone richiesto
    while(curr != NULL){
        if(curr->persone == persone){
            if((prezzo_minimo == -1) || (curr->prezzo < prezzo_minimo)){
                prezzo_minimo = curr->prezzo;
                economico = curr; //memorizza l'appartamento attuale come più economico
                prec_economico = prec;
            }
        }
        prec = curr;
        curr = curr->next;
    }

    //se non ci sono appartamenti sufficienti
    if(economico == NULL){
        return;
    }

    if(prec_economico == NULL){ //l'appartamento più economico è quello in testa
        L = L->next;
    }

    delete economico;
}

double prezzo_tot(lista L, int persone, int giorni){
    double prezzo_totale = 0.0;

    // 1. Controlliamo se esiste un singolo appartamento che può ospitare tutte le persone
    lista curr = L;
    double prezzo_migliore = -1; // Prezzo minimo trovato per un singolo appartamento
    bool trovato_singolo = false;

    while(curr != NULL){
        if(curr->persone >= persone){
            double prezzo_corrente = curr->prezzo * giorni;
            if((prezzo_migliore == -1) || (prezzo_corrente < prezzo_migliore)){
                prezzo_migliore = prezzo_corrente;
                trovato_singolo = true;
            }
        }
        curr = curr->next;
    }

    // Se esiste un singolo appartamento adatto, restituiamo il prezzo più conveniente
    if(trovato_singolo){
        return prezzo_migliore;
    }

    // 2. Se non esiste un singolo appartamento, sommiamo il costo di più appartamenti
    int persone_rimaste = persone;

    while((curr != NULL) && (persone_rimaste > 0)){
        prezzo_totale += curr->prezzo * giorni;
        persone_rimaste -= curr->persone;
        curr = curr->next;
    }

    // 3. Se alla fine ci sono ancora persone senza alloggio, non è possibile soddisfare la richiesta
    if(persone_rimaste > 0){
        return 0.0;
    }

    return prezzo_totale;
}


class Stanza{
    protected: 
     int letti;
     int persone;
     double costo;

    public:
     Stanza(int l, int p, double c){
        letti = l;
        persone = p;
        costo = c;
     }
     double calcola_costo_giornaliero(){
        return costo * (letti + ((double)persone/letti) - 1);
     }

     
};


class Bungalow : public Stanza{
    protected:
     double costo_ombrellone;
     double perc;
    
    public:
     Bungalow(double co, double pe, int l, int p, double c) : Stanza(l, p, c){
        costo_ombrellone = co;
        perc = pe;
     }
     double calcola_costo_giornaliero(){
        double costo_base = Stanza::calcola_costo_giornaliero();
        double costo_maggiorato = costo_base * (1 + perc / 100.0); //costo in percentuale
        return costo_maggiorato + costo_ombrellone ;
     }
};