typedef struct {
    int* x;
    int y;
} Position;

typedef struct {
    Position* super;
    int z;
} _3DPosition;

int main(int argc, char** argv)
{
    print("Hello, World!");
    print("How are you today?");
    printf("You gave me '%d' arguments", argc);
    Position* pos = malloc(sizeof(Position));
    _3DPosition* _3dpos = malloc(sizeof(_3DPosition));
    return;
}
