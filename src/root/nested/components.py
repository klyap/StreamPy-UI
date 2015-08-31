if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
         
from random import randint
from Stream import Stream
from Stream import _no_value
from Operators import stream_func
 
def generate_stream_of_random_integers(stream_length = 10,
                                       max_integer = 100):
    output_stream = Stream()
    random_list = [randint(0, max_integer) for _ in range(stream_length)]
    output_stream.extend(random_list)
    return output_stream
 
def split_into_even_odd(input_stream):
 
    def number_even_odd(m):
            if not m%2:
                return [_no_value, m]
            else:
                return [m, _no_value]
 
    return stream_func(inputs=input_stream,
                       f_type='element',
                       f=number_even_odd,
                       num_outputs=2)
    
def print_stream(stream):
        name = stream.name
         
        def print_stream_value(v, index):
            print name + '[' , index , '] = ', v
            return (_no_value, index+1)
 
        return stream_func(
            inputs=stream,
            f_type='element',
            f=print_stream_value,
            num_outputs=1,
            state=0
            )

# Write values of the stream to a file
def write_stream(stream):
    name = stream.name
    

    def write_stream_value(v, index):
        output_file_name = 'stream_vals.csv'
        f = open(output_file_name, 'a')
        f.write(name + '[' + str(index) + '] = ' + str(v) +',\n')
        f.close()
        return (_no_value, index+1)

    return stream_func(
        inputs=stream,
        f_type='element',
        f=write_stream_value,
        num_outputs=1,
        state=0
        )

def multiply_elements_in_stream(stream, multiplier):
    def mult(v):
        return multiplier*v
    return stream_func(stream, f_type = 'element', f=mult, num_outputs = 1)

 
        