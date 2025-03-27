

class Tools:

    @staticmethod    
    def car_calculator(part1 : str, part2:str) -> int:
        parts  = { "special wheel" : 1000, "super battery":2000 }
        
        sum : int = 0
        
        try:
            sum += parts[part1]
        except:
            raise ValueError('Part not defined')
        
        try:
            sum += parts[part2]
        except:
            raise ValueError('Part not defined')
        
        return sum
    @staticmethod    
    def car_complex_calculator(parts:list[str]) -> int:
        part_database  = { "special wheel" : 1000, "super battery":2000 }
        
        sum : int = 0
        for part in parts:
            try:
                sum += part_database[part]
            except:
                raise ValueError('Part not defined')
        
        return sum