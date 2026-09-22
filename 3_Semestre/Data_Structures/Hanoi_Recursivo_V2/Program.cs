using System;

namespace StackDev
{
    internal class Program
    {
        public static IStack<int> A;
        public static IStack<int> B;
        public static IStack<int> C;

        static HanoiView vista;

        // Mueve un disco de una torre a otra
        static void MoverDisco(IStack<int> origen, IStack<int> destino)
        {
            vista.Mover(origen, destino);
        }

        // Algoritmo recursivo de las Torres de Hanoi
        static void Hanoi(
            int discos,
            IStack<int> TO,
            IStack<int> TA,
            IStack<int> TD)
        {
            if (discos == 1)
            {
                MoverDisco(TO, TD);
            }
            else
            {
                Hanoi(discos - 1, TO, TD, TA);

                MoverDisco(TO, TD);

                Hanoi(discos - 1, TA, TO, TD);
            }
        }

        static void Main()
        {
            Console.WriteLine("Torres de Hanoi");
            Console.WriteLine("Numero de discos:");

            int d = int.Parse(Console.ReadLine());

            // Creamos las tres torres
            // A ya se crea llena con los discos 1, 2, 3... d
            A = new StaticStack<int>(d, 1);

            // B y C empiezan vacias
            B = new StaticStack<int>(d);
            C = new StaticStack<int>(d);


            // Creamos la animacion
            vista = HanoiView.Crear(
                new IStack<int>[] { A, B, C },
                d
            );

            if (vista == null)
            {
                throw new Exception("Terminal chica");
            }

            vista.Iniciar();

            // A = origen
            // B = auxiliar
            // C = destino
            Hanoi(d, A, B, C);

            // Terminamos la animacion
            vista.Terminar();

        }
    }
}