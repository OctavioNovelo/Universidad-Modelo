namespace StackDev
{
    internal interface IStack<T>
    {
        int Size { get; } // Ver tamano
        bool Empty { get; } // Ver si esta vacio
        bool Full { get; } // Ver si esta lleno


        void Push(T e); // Agrega un valor
        T Pop (); // Quitar ultimo valor
        T Peek(); // Ver ultimo valor
        
        #if DEBUG
        string DataPeek();
        #endif
    }
}