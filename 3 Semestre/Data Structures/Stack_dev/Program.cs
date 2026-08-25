// See https://aka.ms/new-console-template for more information

// Una clase static permite acceder a la informacion de una clase SIN tener que
// crear un objeto de esa clase (<class> <nombre> = new ......)


// ADT (Abstract Data Transfer)
// Herramienta que tiene un lenguaje para imlementar un objeto sin especiicar 
// su implementavion

namespace StackDev
{
    internal class Program
    {
        static void Main(string[] args)
        {
            StaticStack stack = new StaticStack();
            stack.Push(5);
        }
    }
}