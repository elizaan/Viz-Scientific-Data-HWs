import struct

def read_dat_and_convert_to_raw(dat_file_path, raw_file_path):
    # Open the .dat file to read binary data
    with open(dat_file_path, 'rb') as dat_file:
        # Read the header
        header = dat_file.read(6)
        x_size, y_size, z_size = struct.unpack('<3H', header)  # Assuming little endian

        # Prepare to read the actual data
        num_voxels = x_size * y_size * z_size
        raw_data = bytearray()

        # Read each 16-bit slice-wise value, noting that only 12 bits are used
        for _ in range(num_voxels):
            # Read 2 bytes (16 bits)
            data_bytes = dat_file.read(2)
            # Convert to 16-bit short, assuming little endian
            data_value = struct.unpack('<H', data_bytes)[0]
            # Mask the lower 12 bits since only those are used
            data_value &= 0xFFF
            # Re-pack as unsigned short (16 bits) and add to raw_data
            raw_data.extend(struct.pack('<H', data_value))

        # Write the processed data to the RAW file
        with open(raw_file_path, 'wb') as raw_file:
            raw_file.write(raw_data)


if __name__ == '__main__':
    read_dat_and_convert_to_raw("/Users/ishratjahaneliza/Documents/CS 6635/code/Viz for scientific data/hw3/data/stagbeetle208x208x123.dat",
                       "/Users/ishratjahaneliza/Documents/CS 6635/code/Viz for scientific data/hw3/data/stagbeetle208x208x123.raw")
    read_dat_and_convert_to_raw("/Users/ishratjahaneliza/Documents/CS 6635/code/Viz for scientific data/hw3/data/footbones832x832x494.dat",
                          "/Users/ishratjahaneliza/Documents/CS 6635/code/Viz for scientific data/hw3/data/footbones832x832x494.raw")
    

