using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Runtime.ExceptionServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using static System.Console;

namespace StackDev
{

    internal class Program
    {
        //La animacion. Si es null (terminal muy chica, salida redirigida...) los movimientos se imprimen como texto
        static HanoiView vista;

        //Mueve el disco de arriba de "origen" a "destino".
        //TODOS los movimientos pasan por aqui para que la animacion los vea
        static void MoverDisco(IStack<int> origen, int torreOrigen, IStack<int> destino, int torreDestino)
        {
            if (vista != null)
            {
                vista.Mover(origen, destino);   //mueve el disco de verdad Y lo anima
            }
            else
            {
                destino.Push(origen.Pop());
                Imprimir(torreOrigen, torreDestino);
            }
        }

        //Mueve n_discos de A a C usando B de auxiliar
        static void Mover(int n_discos, 
            IStack<int> A, int torreA, 
            IStack<int> C, int torreC,
            IStack<int> B, int torreB)
        {
            if (n_discos == 1)
            {
                MoverDisco(A, torreA, C, torreC);
            } 
            else
            { 
                Mover(n_discos - 1, A, torreA, B, torreB, C, torreC);   //los n-1 de arriba se van a B
                MoverDisco(A, torreA, C, torreC);                       //el disco grande se va a C (antes solo se imprimia, no se movia)
                Mover(n_discos - 1, B, torreB, C, torreC, A, torreA);   //los n-1 se van de B a C
            }
        }

        static void Imprimir(int A, int C)
        {
            WriteLine($"{A} -> {C}");
        }

        static void PrintStackStatus<T>(IStack<T> stack)
        {
            #if DEBUG
            WriteLine(stack.DataPeek());
            #endif

            if (stack is ArrayStack<T>)
            {
                ArrayStack<T> astack = stack as ArrayStack<T>;
                WriteLine($"C: {astack.Capacity}, S: {stack.Size}, E: {stack.Empty}, F: {stack.Full}");
            }
            else
            {
                WriteLine($"E: {stack.Empty}, F: {stack.Full}");
            }

            WriteLine();
        }

        static void Main(string[] args)
        {
            WriteLine("Torre Hanoi recursiva");
            WriteLine("Ingrese el numero de discos:");

            int discos;
            while (true)
            {
                string entrada = ReadLine();
                if (entrada == null)   //ya no hay mas entrada (Ctrl+D, archivo terminado...): no seguimos preguntando
                {
                    return;
                }

                if (int.TryParse(entrada, out discos) && discos >= 1)
                {
                    break;
                }

                WriteLine("Escribe un numero entero mayor o igual a 1:");
            }

            // No hay limite de discos, pero con n discos hacen falta 2^n - 1 movimientos:
            // se duplican con cada disco que se agrega, asi que avisamos antes de empezar
            if (discos > 20)
            {
                WriteLine($"{discos} discos son {HanoiView.TextoTotal(discos)} movimientos.");
                WriteLine("Continuar? (s/n)");
                string respuesta = ReadLine();
                if (respuesta == null || !respuesta.Trim().StartsWith("s", StringComparison.OrdinalIgnoreCase))
                {
                    return;
                }
            }

            IStack<int> uno = new StaticStack<int>(discos, 1);
            IStack<int> dos = new StaticStack<int>(discos);
            IStack<int> tres = new StaticStack<int>(discos);

            // Preparamos la animacion (si no cabe en la terminal, vista queda en null y se imprimen los movimientos)
            vista = HanoiView.Crear(new IStack<int>[] { uno, dos, tres }, discos);
            if (vista == null)
            {
                throw new Exception("Terminal chica");
            }
            else
            {
                vista.Iniciar();
            }

            // De la torre 1 a la 3, usando la 2 de auxiliar
            // La recursion baja "discos" niveles ANTES de hacer el primer movimiento, y cada nivel usa
            // memoria de la pila de llamadas. La pila normal (1 MB en Windows, 8 MB en Linux) se acaba
            // con unos miles de discos y el programa se cae, asi que corremos la recursion en un hilo
            // con una pila de 256 MB (alcanza para millones de niveles).
            Thread hilo = new Thread(() => Mover(discos, uno, 1, tres, 3, dos, 2), 256 * 1024 * 1024);
            hilo.Start();
            hilo.Join();   //esperamos a que termine antes de seguir

            // Cerramos la animacion y mostramos el resultado
            if (vista != null)
            {
                vista.Terminar();
            }

            WriteLine("\nListo :)");
        }

    }
}
