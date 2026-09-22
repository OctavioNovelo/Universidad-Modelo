namespace Hanoi
{
    internal class Program
    {
        public static Stack<int> A = new Stack<int>();
        public static Stack<int> B = new Stack<int>();
        public static Stack<int> C = new Stack<int>();
        
        static void Hanoi(int discos, Stack<int> TO, Stack<int> TA, Stack<int> TD)
        {
            if (discos == 1)
            {
                TD.Push(TO.Pop());
            }
            else
            {
                Hanoi(discos - 1, TO, TD, TA);
                TD.Push(TO.Pop());
                Hanoi(discos - 1, TA, TO, TD);
            }
        }

        static void ImprimirStack(string nombre, Stack<int> pila)
        {
            Console.Write($"{nombre}: [");
            foreach (int disco in pila)
            {
                Console.Write(disco + " ");
            }
            Console.WriteLine("]");
        }   

        static void Main()
        {
            Console.WriteLine("Torres de Hanoi\n");
            Console.WriteLine("Numero de discos:");
            int d = int.Parse(Console.ReadLine());

            for (int i = d; i >= 1; i--)
            {
                A.Push(i);
            }

            ImprimirStack("A", A);
            ImprimirStack("B", B);
            ImprimirStack("C", C);


            Hanoi(d, A, B, C);
            Console.WriteLine("Espera papu\n");
            
            ImprimirStack("A", A);
            ImprimirStack("B", B);
            ImprimirStack("C", C);
        }
    }
}