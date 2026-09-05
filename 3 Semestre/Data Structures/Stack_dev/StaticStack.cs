using System;
using System.Data;

namespace StackDev
{
    internal class StaticStack<T> : IStack<T>
    {

        private T[] data;
        private int index;
        public int Size => index + 1;
        public bool Empty => index == -1;
        public bool Full => index == data.Length - 1;


        public StaticStack(int capacity)
        {
            data = new T[capacity];
            index = -1;
        }

        public T Peek()
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

            return data[index--];
        }

        public void Push (T e)
        {
            if (Full)
            {
                throw new IndexOutOfRangeException("index");
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