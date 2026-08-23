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
        static void swap(ref int m, ref int n)
        {
            int aux = 0;
            m = n;
            n = aux;
        }

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