using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace StackDev
{
    internal interface IStack<T>  //aquella clase que se diga que es un stack debe tener estos métodos
    {
        int Size {  get; } //Tamaño de los datos
        bool Empty {  get; } //Ver si esta vacio
        bool Full {  get; }  //Ver si esta lleno

        void Push(T e); //Agregar
        T Pop(); //Eliminar
        T Peek();  //Ver
        T PeekAt(int nivel); //Ver el elemento que esta en la posicion nivel (0 = el del fondo). La usa la animacion para dibujar

        #if DEBUG
        string DataPeek();
        #endif
    }
}
