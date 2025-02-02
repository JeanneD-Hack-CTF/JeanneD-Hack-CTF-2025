#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <stdbool.h>

#define INITIAL_SIZE 10000
#define MULT 2

#define MPEG_VER_1 0
#define MPEG_VER_2 1  
#define MPEG_VER_25 2   
#define MPEG_VER_INVALID -1

#define LAYER_1 0
#define LAYER_2 1
#define LAYER_3 2

// Les deux fonctions suivantes servent à modifier la valeur trouvé 
// pour le Layer et MPEG de façon que l'on puisse utiliser les tableaux 
// si dessous intuitivement.
int b(int bitrate);
int l(int layer);

int bitrate_tab[3][3][16] = {
    // MPEG 1
    {{1, 32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448, 0}, // Layer I
        {1, 32, 48, 56, 64,  80,  96,  112, 128, 160, 192, 224, 256, 320, 384, 0}, // Layer II
        {1, 32, 40, 48, 56,  64,  80,  96,  112, 128, 160, 192, 224, 256, 320, 0} }, // Layer III
    // MPEG 2
    {{1, 32, 48, 56, 64,  80,  96,  112, 128, 144, 160, 176, 192, 224, 256, 0},
        {1, 8,  16, 24, 32,  40,  48,  56,  64,  80, 96, 112, 128, 144, 160, 0},  
        {1, 8,  16, 24, 32,  40,  48,  56,  64,  80, 96, 112, 128, 144, 160, 0}},
    // MPEG 2.5
    {{1, 32, 48, 56, 64,  80,  96,  112, 128, 144, 160, 176, 192, 224, 256, 0}, 
        {1, 8,  16, 24, 32,  40,  48,  56,  64,  80, 96, 112, 128, 144, 160, 0},  
        {1, 8,  16, 24, 32,  40,  48,  56,  64,  80, 96, 112, 128, 144, 160, 0}}
};



int samplerate_matrix[3][3] = {
    {44100, 22050, 11025}, // MPEG 1
    {48000, 24000, 12000}, // MPEG 2
    {32000, 16000, 8000},  // MPEG 2.5
};


// Calcul la taille de la frame.
static int framelength(int layer, int padding, int samplerate, int bitrate) {
    if (layer == LAYER_1) {
        return (12 * bitrate / samplerate + padding) *4;
    } else {
        return (144 * bitrate / samplerate) + padding;
    }
}

int main(int argc, char **argv) {
	if(argc != 2) {
		fprintf(stderr, "Usage: %s <filename.mp3>\n", argv[0]);
		exit(EXIT_FAILURE);
	}
	bool nfind = true;
    FILE *f = fopen(argv[1], "rb"); 
    if (f == NULL) {
        perror("fopen");
        exit(EXIT_FAILURE);
    }
    FILE *flag = fopen("flag.png", "wb"); 
    if (flag == NULL) {
        perror("fopen");
        fclose(f);
        exit(EXIT_FAILURE);
    }

    uint8_t buff[4];
    size_t size = INITIAL_SIZE;
    char *s = malloc((size_t)INITIAL_SIZE + 1); 
    char *q = s;
    if (s == NULL) {
        perror("malloc");
        fclose(f);
        fclose(flag);
        return EXIT_FAILURE;
    }
    while (fread(buff, 1, 4, f) == 4) {
		//On a ici potentiellement un header de frame 
        if ((buff[0] == 0xFF) && ((buff[1] & 0xE0) == 0xE0)) {
            int version = b((buff[1] & 0x18) >> 3); // bits 12,13
            int layer = l((buff[1] & 0x06) >> 1); // bits 14,15
            int bitrate = 1000 * bitrate_tab[version][layer][(buff[2] & 0xF0) >> 4];
            int samplerates = samplerate_matrix[version][(buff[2] & 0x0C) >> 2]; // bits 21,22
            int padding = (buff[2] & 0x02) >> 1; // bit 23
	    

	   //On vérifie que la frame est valide.
	   //Bitrate ne doit pas valoir 0 ou 1000, dans le cas échéant le bitrate n'est pas mentionée. 
            bool is_valid = (version != MPEG_VER_INVALID && layer != -1 && bitrate>= 8000);
            if (is_valid) {
			size_t sz = (size_t)(q-s);
			if ((size_t)(q - s) >= size) {
				char *s2 = realloc(s, size * MULT);
				if (s2 == NULL) {
					perror("realloc");
					free(s); 
					return EXIT_FAILURE;
				}
				s = s2; 
				q = s + sz; 
				size *= MULT;
			}
			// On écrit dans s tout les Private Bits du fichier 
			// signal.mp3
		    	// On récupère la valeur du dernier bit du 3ème octet (24 ème bit du header)
		        int private_bit = (buff[2] & 1);
			*q = private_bit ? '1' : '0'; 
			++q; 
			nfind = false;
			int length = framelength(layer, padding, samplerates, bitrate);
			fseek(f, length - 4, SEEK_CUR);
		}
			
		// nfind sert à s'assurer que après l'instruction 
		// fseek(f,length - 4, SEEK_CUR), les 4 octects lus sont 
		// un header de frame valide validant 
		// le calcul fait dans framelength. 
        } else {
	    if(nfind) {
            	fseek(f, -3, SEEK_CUR); 
	    } 
	    else {
		fprintf(stderr,"Fichier corompue.");
		exit(EXIT_FAILURE);
	    }
      }
    }
    *q = '\0';
    //IHDR et IEND convertit en binaire.
    const char *start_png = "1000100101010000010011100100011100001101000010100001101000001010";	 
    const char *end_png = "00000000000000000000000000000000100100101000101010011100100010010101110010000100110000010000010";
    char *start_offset = strstr(s, start_png);
    char *end_offset = strstr(s, end_png);
    char *p = start_offset;
    char octet[9]; 
    size_t j = 0;
    
    while (p < end_offset + strlen(end_png)) {
        if (j < 8) { 
            octet[j] = *p; 
            j++;
        }
        if (j == 8) {
            octet[j] = '\0'; 
            uint8_t byte = (uint8_t) strtol(octet, NULL, 2); 
            fwrite(&byte, sizeof(uint8_t), 1, flag); 
            j = 0;
        }
        p++; 
    }
    free(s); 
    fclose(f);
    fclose(flag); 
    return 0;
}


int b(int bitrate) {
	switch(bitrate) {
		case(0) :
			return MPEG_VER_25;
			break;
		case(1) : 
			return MPEG_VER_INVALID;
			break;
		case(2) :
			return MPEG_VER_2;
			break;
		case(3) :
			return MPEG_VER_1;
			break;
		default : 
			return -1;
	}
	return -1;
	
}
int l(int layer) {
		switch(layer) {
		case(0) :
			return -1;
		case(1) : 
			return LAYER_3;
		case(2) :
			return LAYER_2;
		case(3) :
			return LAYER_1;
	}
	return -1;
}
