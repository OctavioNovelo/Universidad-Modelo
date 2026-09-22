using System;
using System.Data;

namespace StackDev
{
    internal class ArrayStack<T> : IStack<T>
    {

        // Atributos
        private const int INITIAL_CAPACITY = 4;
        private T[] data;
        private int index;

        // Al convertir el set en privado, capacity solo puede ser asignado dentro de ArrayStack
        // y no fuera. Pero capacity queda publico.
        public int Capacity { get; private set;}
        public int Size => index + 1;
        public bool Empty => index == -1;
        public bool Full => index == data.Length - 1;

        // Constructor 
        // Las propiedades de solo lectura. Una vez creadas el arreglo no se pueden modifica. 
        // El unico lugar donde se pueden modificar es en el contructuro.
        public ArrayStack()
        {
            Capacity = INITIAL_CAPACITY;
            data = new T[Capacity];
            index = -1;
        }

        public ArrayStack(int capacity)
        {
            // operando de 3 (?)
            // condicion ? valor A (caso true) : valor B (cado false)
            Capacity = capacity < INITIAL_CAPACITY ? INITIAL_CAPACITY : capacity;
            data = new T[Capacity];
            index = -1;    
        }


        // Metodos
        public T Peek ()
        {
            if (Empty)
            {
                throw new IndexOutOfRangeException("index");
            }

            return data[index];
        }
        public T Pop()
        {
            if (Empty)
            {
                throw new IndexOutOfRangeException("index");
            }

            if (Capacity / 2 >= INITIAL_CAPACITY && index == Capacity / 5)
            {
                T[] newData = new T[Capacity/2];
                Array.Copy(data, newData, Size);

                Capacity /= 2;
                data = newData;
            }

            return data[index--];

        }
        public void Push (T e)
        {
            if (Full)
            {   
                T[] newData = new T[Capacity*2];
                Array.Copy(data, newData, Capacity);
                data = newData;
            }

            data[++index] = e;
        }

        #if DEBUG
        public string DataPeek()
        {
            string aux = "[";
            
            for (int i = 0; i <= Size; i++)
            {
                aux += $" {data[i]}";
            }
            aux += "]";

            return aux;
        }
        #endif
    }
}