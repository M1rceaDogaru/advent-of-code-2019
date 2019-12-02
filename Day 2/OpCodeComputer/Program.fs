// Learn more about F# at http://fsharp.org

open System
open System.IO

type OpCodeEngine() =
    member x.GetOpCodes(path: string) =
        let opCodes = File.ReadAllText(path)
        opCodes.Split ','
    member x.ProcessOpCodes(opCodes: string[]) =
        let mutable index = 0
        let mutable stop = false

        while not stop && index < opCodes.Length do
            match opCodes.[index] with
            | "1" -> opCodes.[opCodes.[index + 3] |> int] <- ((opCodes.[opCodes.[index + 1] |> int] |> int) + (opCodes.[opCodes.[index + 2] |> int] |> int)).ToString()
            | "2" -> opCodes.[opCodes.[index + 3] |> int] <- ((opCodes.[opCodes.[index + 1] |> int] |> int) * (opCodes.[opCodes.[index + 2] |> int] |> int)).ToString()
            | "99" -> stop <- true

            index <- index + 4        
        opCodes
    member x.GetOpValuesForInput(input: int, opCodes: string[]) =
        let mutable resultNoun = 0
        let mutable resultVerb = 0

        for noun in [|0..99|] do
            for verb in [|0..99|] do
                let memory = Array.copy opCodes
                memory.[1] <- noun.ToString()
                memory.[2] <- verb.ToString()
                let result = x.ProcessOpCodes(memory).[0] |> int
                if result = input then
                    resultNoun <- noun |> int
                    resultVerb <- verb |> int
        
        100 * resultNoun + resultVerb

let challenge_1() =
    let opCodeEngine = OpCodeEngine()
    let opCodes = opCodeEngine.GetOpCodes(@"input.txt")
    let processedOpCodes = opCodeEngine.ProcessOpCodes(opCodes)

    printfn "Value at position 0 is %s" processedOpCodes.[0]

let challenge_2() =
    let opCodeEngine = OpCodeEngine()
    let opCodes = opCodeEngine.GetOpCodes(@"input.txt")

    let result = opCodeEngine.GetOpValuesForInput(19690720, opCodes)
    printfn "100 * noun + verb = %s" (result.ToString())

[<EntryPoint>]
let main argv =
    challenge_1()
    challenge_2()

    Console.ReadLine() |> ignore
    0 // return an integer exit code


