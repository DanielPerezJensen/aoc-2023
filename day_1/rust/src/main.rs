const _TEST1: &'static str = include_str!("test1.txt");
const _TEST2: &'static str = include_str!("test2.txt");
const _DATA: &'static str = include_str!("data.txt");

fn part1(input: &str) -> u32 {
    let mut solution: u32 = 0;

    for line in input.lines() {
        let mut first: u32 = 0;
        let mut second: u32 = 0;

        for ch in line.chars() {
            if ch.is_ascii_digit() {
                first = ch.to_digit(10).unwrap();
                break;
            }
        }

        for ch in line.chars().rev() {
            if ch.is_ascii_digit() {
                second = ch.to_digit(10).unwrap();
                break;
            }
        }

        solution = solution + first * 10 + second
        // let mut lines = input.lines();
    }
    return solution;
}

fn main() {
    let result = part1(_TEST1);
    println!("Part 1: {}", result);
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn part1_test() {
        assert_eq!(part1(_TEST1), 142)
    }
}
