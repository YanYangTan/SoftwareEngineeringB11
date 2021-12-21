export declare type Formatter<T> = (item: T) => string;
export interface FormatterMap<T> {
    [key: string]: Formatter<T>;
}
export interface FormatSection<T> {
    size: number;
    formats: FormatterMap<T>;
}
export interface FormatEscapes {
    [first: string]: {
        start: string;
        startEscape: string;
        end: string;
        endEscape: string;
    };
}
export declare class Format<T> {
    private cached;
    private sections;
    private escapes;
    constructor(formats: FormatterMap<T>, escapes?: FormatEscapes);
    add(map: FormatterMap<T>): this;
    add(key: string, formatter: Formatter<T>): this;
    getSection(size: number): FormatSection<T>;
    private sortBySize;
    private getEscaped;
    getFormatter(format: string, cache?: boolean): Formatter<T>;
    format(format: string, item: T, cache?: boolean): string;
}
