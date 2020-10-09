// This overview of modules may be helpful:
// https://www.typescriptlang.org/docs/handbook/modules.html  

export interface SocketType {
    on: (eventName: string, callback: any) => (any);
    emit: (tag: string, data: any) => void;
}