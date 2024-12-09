
Sequence
    together
        do for 5 seconds
            beep every second
        end

        do for 5 seconds
            move forward at speed x
        end
    end
    do for 5 seconds
        beep for 5 seconds
    end
end


if not beeping:
    store start of interval
else
    start beep
    
