# Scenario 1: A1 A2 B1 B2
counter = 10
# Process A
r0_a = counter  # A1: LD(counter, R0)
r0_a += 1       # ADDC(R0, 1, R0)
counter = r0_a  # A2: ST(R0, counter)
# Process B
r0_b = counter  # B1: LD(counter, R0)
r0_b += 2       # ADDC(R0, 2, R0)
counter = r0_b  # B2: ST(R0, counter)
print(f"A1 A2 B1 B2: counter = {counter}")

# Scenario 2: A1 B1 A2 B2
counter = 10
# Processes load concurrently
r0_a = counter  # A1: LD(counter, R0)
r0_b = counter  # B1: LD(counter, R0)
# Process A computes and stores
r0_a += 1       # ADDC(R0, 1, R0)
counter = r0_a  # A2: ST(R0, counter)
# Process B computes and stores
r0_b += 2       # ADDC(R0, 2, R0)
counter = r0_b  # B2: ST(R0, counter)
print(f"A1 B1 A2 B2: counter = {counter}")

# Scenario 3: A1 B1 B2 A2
counter = 10
# Processes load concurrently
r0_a = counter  # A1: LD(counter, R0)
r0_b = counter  # B1: LD(counter, R0)
# Process B computes and stores
r0_b += 2       # ADDC(R0, 2, R0)
counter = r0_b  # B2: ST(R0, counter)
# Process A computes and stores
r0_a += 1       # ADDC(R0, 1, R0)
counter = r0_a  # A2: ST(R0, counter)

print(f"A1 B1 B2 A2: counter = {counter}")
# Scenario 4: B1 A1 B2 A2
counter = 10
# Processes load concurrently
r0_b = counter  # B1: LD(counter, R0)
r0_a = counter  # A1: LD(counter, R0)
# Process B computes and stores
r0_b += 2       # ADDC(R0, 2, R0)
counter = r0_b  # B2: ST(R0, counter)
# Process A computes and stores
r0_a += 1       # ADDC(R0, 1, R0)
counter = r0_a  # A2: ST(R0, counter)
print(f"B1 A1 B2 A2: counter = {counter}")

# Scenario 5: B1 A1 A2 B2
counter = 10
# Processes load concurrently
r0_b = counter  # B1: LD(counter, R0)
r0_a = counter  # A1: LD(counter, R0)
# Process A computes and stores
r0_a += 1       # ADDC(R0, 1, R0)
counter = r0_a  # A2: ST(R0, counter)
# Process B computes and stores
r0_b += 2       # ADDC(R0, 2, R0)
counter = r0_b  # B2: ST(R0, counter)
print(f"B1 A1 A2 B2: counter = {counter}")

# Scenario 6: B1 B2 A1 A2
counter = 10
# Process B
r0_b = counter  # B1: LD(counter, R0)
r0_b += 2       # ADDC(R0, 2, R0)
counter = r0_b  # B2: ST(R0, counter)
# Process A
r0_a = counter  # A1: LD(counter, R0)
r0_a += 1       # ADDC(R0, 1, R0)
counter = r0_a  # A2: ST(R0, counter)
print(f"B1 B2 A1 A2: counter = {counter}")