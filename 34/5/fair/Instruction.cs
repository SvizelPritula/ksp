namespace Fair;

public interface IInstruction { }

public record class MoveInstruction(Node Destination) : IInstruction
{
    public override string ToString()
    {
        return $"P {Destination.Id}";
    }
}

public record class WaitInstruction(long Time) : IInstruction
{
    public override string ToString()
    {
        return $"C {Time}";
    }
}
