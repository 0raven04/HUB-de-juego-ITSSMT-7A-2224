//
//  ContentView.swift
//  pacman
//
//  Created by Lou on 04/11/25.
//

import SwiftUI
import SpriteKit
import AVFoundation

// MARK: - ROOT VIEW CON MENÚ DE INICIO
struct MainView: View {
    @State private var started = false

    var body: some View {
        ZStack {
            LinearGradient(
                gradient: Gradient(colors: [.black, .gray]),
                startPoint: .top, endPoint: .bottom
            )
            .ignoresSafeArea()

            if !started {
                VStack(spacing: 30) {
                    Text("PACMAN")
                        .font(.system(size: 48, weight: .bold, design: .rounded))
                        .foregroundColor(.yellow)
                        .shadow(radius: 10)

                    Button(action: { started = true }) {
                        Text("Jugar")
                            .font(.system(size: 26, weight: .bold, design: .rounded))
                            .padding(.vertical, 14)
                            .padding(.horizontal, 40)
                            .background(
                                RoundedRectangle(cornerRadius: 16)
                                    .fill(Color.blue)
                            )
                            .foregroundColor(.white)
                            .shadow(radius: 6)
                    }
                }
            } else {
                ContentView()
            }
        }
    }
}

// MARK: - Notificaciones
extension Notification.Name {
    static let playerMove = Notification.Name("playerMove")
    static let gameScoreUpdated = Notification.Name("gameScoreUpdated")
    static let lifeLost = Notification.Name("lifeLost")
    static let gameOver = Notification.Name("gameOver")
    static let gameWon = Notification.Name("gameWon")
}

enum MoveDirection: Int {
    case up = 0, down = 1, left = 2, right = 3
}

// MARK: - CONTENTVIEW ORIGINAL (NO TOCADO)
struct ContentView: View {
    @State private var scene: SKScene = GameScene(size: CGSize(width: 1200, height: 900))
    @State private var score: Int = 0
    @State private var lives: Int = 3
    @State private var isGameOver: Bool = false
    @State private var isPausedGame: Bool = false
    @State private var isGameWon: Bool = false

    var body: some View {
        VStack(spacing: 12) {
            HStack(spacing: 16) {
                VStack(alignment: .leading) {
                    Text("PUNTAJE")
                        .font(.system(size: 14, weight: .semibold, design: .rounded))
                        .foregroundColor(.white)
                    Text("\(score)")
                        .font(.system(size: 18, weight: .bold, design: .rounded))
                        .foregroundColor(.yellow)
                }

                Spacer()

                VStack(alignment: .trailing) {
                    Text("VIDAS")
                        .font(.system(size: 14, weight: .semibold, design: .rounded))
                        .foregroundColor(.white)
                    HStack(spacing: 8) {
                        ForEach(0..<max(0, lives), id: \.self) { _ in
                            Circle()
                                .frame(width: 12, height: 12)
                                .foregroundColor(.yellow)
                                .overlay(Circle().stroke(Color.white.opacity(0.2), lineWidth: 1))
                        }
                    }
                }

                Button(action: togglePause) {
                    Text(isPausedGame ? "Reanudar" : "Pausa")
                        .font(.system(size: 14, weight: .semibold))
                        .frame(width: 90, height: 36)
                        .background(RoundedRectangle(cornerRadius: 10).fill(Color(.systemGray6)))
                }
            }
            .padding(.horizontal, 18)

            GeometryReader { geo in
                SpriteView(scene: scene)
                    .ignoresSafeArea(edges: .bottom)
                    .frame(width: geo.size.width, height: geo.size.height * 0.78)
                    .cornerRadius(12)
                    .shadow(radius: 8)
            }
            .frame(height: 620)

            if isGameOver {
                Text("GAME OVER")
                    .font(.system(size: 20, weight: .semibold, design: .rounded))
                    .foregroundColor(.red)
            }

            if isGameWon {
                Text("GANASTE: Completaste todas las frutas")
                    .font(.system(size: 18, weight: .semibold, design: .rounded))
                    .foregroundColor(.green)
            }

            HStack(spacing: 20) {
                Button(action: { sendControl(.left) }) { controlButton("IZQ") }
                VStack(spacing: 12) {
                    Button(action: { sendControl(.up) }) { controlButton("ARR") }
                    Button(action: { sendControl(.down) }) { controlButton("ABA") }
                }
                Button(action: { sendControl(.right) }) { controlButton("DER") }

                Spacer()

                Button(action: { restartGame(fullReset: true) }) {
                    Text("Reiniciar")
                        .font(.system(size: 16, weight: .semibold))
                        .frame(width: 120, height: 44)
                        .background(RoundedRectangle(cornerRadius: 10).fill(Color.blue))
                        .foregroundColor(.white)
                }
            }
            .padding(.horizontal, 18)
            .padding(.bottom, 8)
        }
        .background(LinearGradient(gradient: Gradient(colors: [Color.black, Color(.darkGray)]), startPoint: .top, endPoint: .bottom))
        .onReceive(NotificationCenter.default.publisher(for: .gameScoreUpdated)) { n in
            if let s = n.userInfo?["score"] as? Int { score = s }
        }
        .onReceive(NotificationCenter.default.publisher(for: .lifeLost)) { n in
            if let remaining = n.userInfo?["lives"] as? Int { lives = remaining }
        }
        .onReceive(NotificationCenter.default.publisher(for: .gameOver)) { _ in
            isGameOver = true
        }
        .onReceive(NotificationCenter.default.publisher(for: .gameWon)) { _ in
            isGameWon = true
        }
    }

    func controlButton(_ text: String) -> some View {
        Text(text)
            .font(.system(size: 18, weight: .bold))
            .frame(width: 64, height: 44)
            .background(RoundedRectangle(cornerRadius: 10).fill(Color(.systemGray6)))
    }

    func sendControl(_ dir: MoveDirection) {
        NotificationCenter.default.post(name: .playerMove, object: nil, userInfo: ["dir": dir.rawValue])
    }

    func restartGame(fullReset: Bool) {
        isGameOver = false
        isGameWon = false
        if fullReset {
            lives = 3
        }
        if let gs = scene as? GameScene {
            gs.restart(fullReset: fullReset)
        } else {
            scene = GameScene(size: CGSize(width: 1200, height: 900))
        }
    }

    func togglePause() {
        isPausedGame.toggle()
        if let gs = scene as? GameScene {
            gs.setPaused(isPausedGame)
        }
    }
}

// MARK: - GAME SCENE COMPLETA (SIN CAMBIOS)
class GameScene: SKScene {
    private var grid: [[Int]] = [
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,1],
        [1,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,1],
        [1,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,0,1,1,1,1,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,1],
        [1,0,1,1,0,1,1,0,0,1,1,0,0,0,0,0,1],
        [1,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
        [1,0,0,1,1,1,0,1,1,1,0,1,1,0,0,0,1],
        [1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

    private var tileSize: CGSize = .zero
    private var origin: CGPoint = .zero

    private var playerNode: SKShapeNode!
    private var ghostNodes: [SKShapeNode] = []

    private var playerPos = (x: 1, y: 1)
    private var ghostsPos: [(x: Int, y: Int)] = [(15,1),(15,5),(12,8)]

    private var score = 0
    private var lives = 3
    private var ghostTimer: Timer?

    private var bgPlayer: AVAudioPlayer?
    private var eatPlayer: AVAudioPlayer?
    private var deathPlayer: AVAudioPlayer?

    private var mouthOpen: Bool = true
    private var mouthActionKey = "mouthAction"

    override init(size: CGSize) {
        super.init(size: size)
        scaleMode = .resizeFill
        anchorPoint = CGPoint(x: 0.5, y: 0.5)
        backgroundColor = .black
        NotificationCenter.default.addObserver(self, selector: #selector(handlePlayerMove(_:)), name: .playerMove, object: nil)
        setupAudio()
        setupScene()
    }

    required init?(coder aDecoder: NSCoder) { super.init(coder: aDecoder) }

    deinit {
        NotificationCenter.default.removeObserver(self)
        ghostTimer?.invalidate()
    }

    func setupAudio() {
        bgPlayer = loadPlayer(named: "music", loops: -1, volume: 0.5)
        eatPlayer = loadPlayer(named: "eat", loops: 0, volume: 1.0)
        deathPlayer = loadPlayer(named: "death", loops: 0, volume: 1.0)
        bgPlayer?.play()
    }

    private func loadPlayer(named name: String, loops: Int, volume: Float) -> AVAudioPlayer? {
        guard let url = Bundle.main.url(forResource: name, withExtension: "mp3")
            ?? Bundle.main.url(forResource: name, withExtension: "wav")
        else { return nil }

        do {
            let p = try AVAudioPlayer(contentsOf: url)
            p.numberOfLoops = loops
            p.volume = volume
            p.prepareToPlay()
            return p
        } catch {
            print("Audio error: \(error)")
            return nil
        }
    }

    func setupScene() {
        removeAllChildren()

        let cols = grid.first?.count ?? 0
        let rows = grid.count

        let availableWidth = size.width * 0.92
        let availableHeight = size.height * 0.9
        let ts = min(availableWidth / CGFloat(cols), availableHeight / CGFloat(rows))
        tileSize = CGSize(width: ts, height: ts)

        let boardWidth = CGFloat(cols) * tileSize.width
        let boardHeight = CGFloat(rows) * tileSize.height
        origin = CGPoint(x: -boardWidth/2 + tileSize.width/2,
                         y: boardHeight/2 - tileSize.height/2)

        for y in 0..<rows {
            for x in 0..<cols {
                let value = grid[y][x]
                let tileColor = (value == 1) ? UIColor.systemBlue : UIColor.black
                let tile = SKSpriteNode(color: tileColor, size: tileSize)
                tile.position = pointForGrid(x: x, y: y)
                tile.zPosition = 0
                addChild(tile)

                if value == 2 {
                    let fruit = SKShapeNode(circleOfRadius: max(4, tileSize.width * 0.12))
                    fruit.fillColor = .systemGreen
                    fruit.strokeColor = .clear
                    fruit.position = pointForGrid(x: x, y: y)
                    fruit.zPosition = 2
                    fruit.name = "fruit_\(x)_\(y)"
                    addChild(fruit)
                }

                let border = SKShapeNode(
                    rectOf: CGSize(width: tileSize.width - 2, height: tileSize.height - 2),
                    cornerRadius: 2
                )
                border.strokeColor = UIColor(white: 1.0, alpha: 0.03)
                border.lineWidth = 1
                border.position = pointForGrid(x: x, y: y)
                border.zPosition = 1
                addChild(border)
            }
        }

        let playerRadius = min(tileSize.width, tileSize.height) * 0.38
        playerNode = SKShapeNode(path: pacmanPath(open: mouthOpen, radius: playerRadius))
        playerNode.fillColor = .yellow
        playerNode.strokeColor = .clear
        playerNode.zPosition = 5
        playerNode.position = pointForGrid(x: playerPos.x, y: playerPos.y)
        addChild(playerNode)
        startMouthAnimation()

        ghostNodes.removeAll()
        let ghostColors: [UIColor] = [.systemRed, .systemTeal, .systemOrange]

        for (i, gpos) in ghostsPos.enumerated() {
            let gn = SKShapeNode(circleOfRadius: playerRadius * 0.95)
            gn.fillColor = ghostColors[i % ghostColors.count]
            gn.strokeColor = .clear
            gn.zPosition = 5
            gn.position = pointForGrid(x: gpos.x, y: gpos.y)
            addChild(gn)
            ghostNodes.append(gn)
        }

        ghostTimer?.invalidate()
        ghostTimer = Timer.scheduledTimer(withTimeInterval: 0.9, repeats: true) { [weak self] _ in
            self?.stepGhosts()
        }
    }

    func pointForGrid(x: Int, y: Int) -> CGPoint {
        CGPoint(
            x: origin.x + CGFloat(x) * tileSize.width,
            y: origin.y - CGFloat(y) * tileSize.height
        )
    }

    func pacmanPath(open: Bool, radius: CGFloat) -> CGPath {
        let path = UIBezierPath()
        let startAngle: CGFloat = open ? (-0.25 * .pi) : (-0.05 * .pi)
        let endAngle: CGFloat = open ? (0.25 * .pi) : (0.05 * .pi)
        path.addArc(withCenter: .zero, radius: radius, startAngle: startAngle, endAngle: endAngle, clockwise: true)
        path.addLine(to: .zero)
        path.close()
        return path.cgPath
    }

    func startMouthAnimation() {
        removeAction(forKey: mouthActionKey)
        let flip = SKAction.run { [weak self] in
            guard let self = self else { return }
            self.mouthOpen.toggle()
            let r = min(self.tileSize.width, self.tileSize.height) * 0.38
            self.playerNode.path = self.pacmanPath(open: self.mouthOpen, radius: r)
        }
        let wait = SKAction.wait(forDuration: 0.18)
        let seq = SKAction.sequence([flip, wait])
        run(SKAction.repeatForever(seq), withKey: mouthActionKey)
    }

    @objc func handlePlayerMove(_ n: Notification) {
        guard let raw = n.userInfo?["dir"] as? Int,
              let dir = MoveDirection(rawValue: raw)
        else { return }

        var nx = playerPos.x
        var ny = playerPos.y

        switch dir {
        case .up: ny -= 1
        case .down: ny += 1
        case .left: nx -= 1
        case .right: nx += 1
        }

        if ny >= 0 && ny < grid.count && nx >= 0 && nx < (grid.first?.count ?? 0) {
            if grid[ny][nx] != 1 {
                movePlayer(to: (nx, ny))
            }
        }
    }

    func movePlayer(to newPos: (x: Int, y: Int)) {
        playerPos = newPos
        let dest = pointForGrid(x: newPos.x, y: newPos.y)
        playerNode.run(SKAction.move(to: dest, duration: 0.15))

        if grid[newPos.y][newPos.x] == 2 {
            grid[newPos.y][newPos.x] = 0

            if let fruit = childNode(withName: "fruit_\(newPos.x)_\(newPos.y)") {
                eatPlayer?.play()
                fruit.run(SKAction.group([
                    SKAction.scale(to: 0, duration: 0.18),
                    SKAction.fadeOut(withDuration: 0.18)
                ])) {
                    fruit.removeFromParent()
                }
            }

            score += 10
            NotificationCenter.default.post(name: .gameScoreUpdated, object: nil, userInfo: ["score": score])
            checkWinCondition()
        }

        checkCollision()
    }

    func stepGhosts() {
        for i in 0..<ghostsPos.count {
            let g = ghostsPos[i]
            if let next = nextStepTowardsTarget(from: g, target: playerPos) {
                ghostsPos[i] = next
                let dest = pointForGrid(x: next.x, y: next.y)
                ghostNodes[i].run(SKAction.move(to: dest, duration: 0.45))
            }
        }
        checkCollision()
    }

    func nextStepTowardsTarget(from start: (x:Int,y:Int), target: (x:Int,y:Int)) -> (x:Int,y:Int)? {
        let rows = grid.count
        let cols = grid.first?.count ?? 0
        var visited = Array(repeating: Array(repeating: false, count: cols), count: rows)
        var queue: [((x:Int,y:Int), [(Int,Int)])] = [ (start, []) ]
        visited[start.y][start.x] = true

        let dirs = [(1,0),(-1,0),(0,1),(0,-1)]

        while !queue.isEmpty {
            let (cur, path) = queue.removeFirst()

            if cur == target {
                return path.first
            }

            for d in dirs {
                let nx = cur.x + d.0
                let ny = cur.y + d.1

                if nx >= 0 && nx < cols &&
                   ny >= 0 && ny < rows &&
                   !visited[ny][nx] &&
                   grid[ny][nx] != 1 {

                    visited[ny][nx] = true
                    var newPath = path
                    newPath.append((nx, ny))
                    queue.append(((nx, ny), newPath))
                }
            }
        }

        return nil
    }

    func checkCollision() {
        for g in ghostsPos where g == playerPos {
            loseLife()
            return
        }
    }

    func loseLife() {
        deathPlayer?.play()
        lives -= 1

        NotificationCenter.default.post(name: .lifeLost, object: nil, userInfo: ["lives": lives])

        if lives <= 0 {
            ghostTimer?.invalidate()
            NotificationCenter.default.post(name: .gameOver, object: nil)
        } else {
            respawnPositions()
        }
    }

    func respawnPositions() {
        playerPos = (1,1)
        playerNode.run(SKAction.move(to: pointForGrid(x: 1, y: 1), duration: 0.18))

        ghostsPos = [(15,1),(15,5),(12,8)]
        for (i, gnode) in ghostNodes.enumerated() {
            gnode.run(SKAction.move(to: pointForGrid(x: ghostsPos[i].x, y: ghostsPos[i].y), duration: 0.25))
        }
    }

    func checkWinCondition() {
        for row in grid { if row.contains(2) { return } }

        ghostTimer?.invalidate()
        NotificationCenter.default.post(name: .gameWon, object: nil)
    }

    func setPaused(_ p: Bool) {
        isPaused = p
        ghostTimer?.invalidate()

        if !p {
            ghostTimer = Timer.scheduledTimer(withTimeInterval: 0.9, repeats: true) { [weak self] _ in
                self?.stepGhosts()
            }
        }
    }

    func restart(fullReset: Bool) {
        score = 0
        if fullReset { lives = 3 }

        NotificationCenter.default.post(name: .gameScoreUpdated, object: nil, userInfo: ["score": score])
        NotificationCenter.default.post(name: .lifeLost, object: nil, userInfo: ["lives": lives])

        setupScene()
    }
}

#if DEBUG
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        MainView()
    }
}
#endif
