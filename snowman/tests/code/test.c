typedef struct _Position Position;
struct _Position {
    int* x;
    int y;
};
typedef struct __3DPosition _3DPosition;
struct __3DPosition {
    Position __super__;
    int z;
};
int main(int argc, char** argv)
{
    print("Hello, World!");
    print("How are you today?");
    printf("You gave me '%d' arguments", argc);
    Position* pos = malloc(sizeof(Position));
    _3DPosition* _3dpos = malloc(sizeof(_3DPosition));
    return;
}
