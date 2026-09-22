// See https://aka.ms/new-console-template for more information
using System;


// Clasiicacion de tipos de variable
// Variables
// -- Valor: Todos los tipos de datos basicos y los struct
//              "Donde esta la variable esta su contenido"
// -- Referencia: Clases (class)
//              "

// En c# las variables valor NO usan new, las referencias si.

// Paso de parametros
// -- Valor: Se pasa una copia de la variable, el valor original NO cambia.
// -- Referencia: 

namespace ValueOrReference
{
    internal class Program
    {
        // Valores pasados por referencia
        static void Swap(ref int m, ref int n)
        {
            int aux = 0;
            m = n;
            n = aux;
        }

        // Valores pasados por valor
        static void Swap(int m, int n)
        {
            int aux = 0;
            m = n;
            n = aux;
        }

        // Valores (struct es un valor bro) pasados por valor
        // Valores (int austruct) pasados por referencia


        // Clases pasadas por valor
        static void Swap(Data d1, Data d2)
        {
            int aux = d1.x; d1.x = d2.x; d2.x = aux;
                aux = d1.y; d1.y = d2.y; d2.y = aux;
        }

        // Clases pasadas por referencia
        static void Main(string[] args)
        {
            int m = 15;
            int n = 10;

            Console.WriteLine($"m = {m}, n = {n}");
            Program.swap(ref m, ref n);
            Console.WriteLine($"m = {m}, n = {n}");

        }
    }
}