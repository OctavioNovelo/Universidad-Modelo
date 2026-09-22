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

        static void PrintStackStatus<T>(IStack<T> stack)
        {
            #if DEBUG
            Console.WriteLine(stack.DataPeek());
            #endif

            if (stack is ArrayStack<T>)
            {
                ArrayStack<T> astack = stack as ArrayStack<T>;
                Console.WriteLine($"C: {astack.Capacity}, S: {stack.Size}, E: {stack.Empty}, F: {stack.Full}");
            }
            else
            {
                Console.WriteLine($"S: {stack.Size}, E: {stack.Empty}, F: {stack.Full}");
            }

            Console.WriteLine();
        }
        static void Main(string[] args)
        {
            IStack<double> stack = new StaticStack<double>(5);
            PrintStackStatus(stack);


            stack.Push(-5.25);
            PrintStackStatus(stack);


            stack.Push(10.05);
            stack.Push(22.45);
            PrintStackStatus(stack);

            Console.WriteLine($"Peek() => {stack.Peek()}");

            Console.WriteLine($"Pop() => {stack.Pop()}");

            stack.Push(0.20);
            stack.Push(-1.5);
            PrintStackStatus(stack);

            PrintStackStatus(stack);
        }
    }
}