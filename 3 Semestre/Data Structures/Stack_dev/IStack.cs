namespace StackDev
{
    internal interface IStack
    {
        int Size { get; } // Ver tamano
        bool Empty { get; } // Ver si esta vacio
        bool Full { get; } // Ver si esta lleno


        void Push(int e); // Agrega un valor
        void Pop (); // Quitar ultimo valor
        void Peek(); // Ver ultimo valor
        
    }
}